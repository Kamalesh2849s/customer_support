from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Tuple

class Action(BaseModel):
    command: str = Field(description="Command to execute: 'ask_customer', 'search_kb', 'query_database', 'route_ticket', or 'resolve_ticket'")
    args: str = Field(description="Arguments for the command. ask_customer: question. search_kb: query. query_database: user_id or ticket_id. route_ticket: department. resolve_ticket: summary.")

class Observation(BaseModel):
    ticket_id: str
    ticket_text: str
    current_knowledge: str = "No additional info gathered."
    last_action_result: str = ""
    is_done: bool = False

class Reward(BaseModel):
    value: float
    reason: str

class State(BaseModel):
    ticket_id: str
    ticket_text: str
    conversation_history: List[str]
    kb_queries: List[str]
    db_queries: List[str]
    step_count: int
    max_steps: int
    is_done: bool
    final_score: float

class SupportTriageEnv:
    def __init__(self, tasks: List[Any] = None):
        if not tasks:
            from tasks.task1_basic_route import Task1BasicRoute
            from tasks.task2_info_gathering import Task2InfoGathering
            from tasks.task3_policy_resolution import Task3PolicyResolution
            from tasks.task4_prompt_injection import Task4PromptInjection
            self.tasks = [
                Task1BasicRoute(),
                Task2InfoGathering(),
                Task3PolicyResolution(),
                Task4PromptInjection()
            ]
        else:
            self.tasks = tasks
        
        self.current_task_idx = 0
        self.current_task = None
        self.state_data = None
        
    def reset(self, *args, **kwargs) -> Tuple[Observation, Dict[str, Any]]:
        task_idx = kwargs.get("task_idx")
        if task_idx is None and "options" in kwargs and isinstance(kwargs["options"], dict):
            task_idx = kwargs["options"].get("task_idx")
            
        if task_idx is not None:
            self.current_task_idx = task_idx
        elif self.tasks and self.current_task_idx >= len(self.tasks):
            self.current_task_idx = 0
            
        if self.tasks:
            self.current_task = self.tasks[self.current_task_idx]
            task_data = self.current_task.get_initial_data()
        else:
            task_data = {"ticket_id": "T-000", "ticket_text": "Sample ticket"}
            
        self.state_data = State(
            ticket_id=task_data["ticket_id"],
            ticket_text=task_data["ticket_text"],
            conversation_history=[],
            kb_queries=[],
            db_queries=[],
            step_count=0,
            max_steps=10,
            is_done=False,
            final_score=0.0
        )
        
        obs = Observation(
            ticket_id=self.state_data.ticket_id,
            ticket_text=self.state_data.ticket_text,
            current_knowledge="No additional info gathered.",
            last_action_result="Environment reset.",
            is_done=False
        )
        return obs, {}
        
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        self.state_data.step_count += 1
        reward = Reward(value=-0.05, reason="Step penalty")
        done = False
        info = {}
        result_text = ""
        current_knowledge = ""
        
        if self.state_data.is_done:
            return self._current_obs(), Reward(value=0.0, reason="Episode already done"), True, {"error": "Episode already done"}
            
        if action.command == "ask_customer":
            self.state_data.conversation_history.append(f"Agent: {action.args}")
            response = self.current_task.handle_ask(action.args) if self.current_task else "No task defined."
            self.state_data.conversation_history.append(f"Customer: {response}")
            result_text = f"Customer replied: {response}"
            
        elif action.command == "search_kb":
            self.state_data.kb_queries.append(f"KB Search: {action.args}")
            result = self.current_task.handle_search(action.args) if self.current_task else "No task defined."
            result_text = f"KB Search Results: {result}"
            if "No relevant articles" not in result:
                reward.value += 0.1
                reward.reason = "Found relevant KB article"
                
        elif action.command == "query_database":
            self.state_data.db_queries.append(f"DB Query: {action.args}")
            if hasattr(self.current_task, "handle_db_query"):
                result = self.current_task.handle_db_query(action.args)
            else:
                result = "No database records found for this user."
            result_text = f"Database Record: {result}"
            reward.value += 0.1
            reward.reason = "Queried Customer Database"
                
        elif action.command == "route_ticket":
            if self.current_task:
                done, score, reason = self.current_task.grade_route(action.args, self.state_data)
            else:
                done, score, reason = True, 0.0, "No task"
            reward.value = score
            reward.reason = reason
            self.state_data.final_score = score
            self.state_data.is_done = True
            result_text = f"Ticket routed. Resolution: {reason}"
            
        elif action.command == "resolve_ticket":
            if self.current_task:
                done, score, reason = self.current_task.grade_resolve(action.args, self.state_data)
            else:
                done, score, reason = True, 0.0, "No task"
            reward.value = score
            reward.reason = reason
            self.state_data.final_score = score
            self.state_data.is_done = True
            result_text = f"Ticket resolved. Resolution: {reason}"
            
        else:
            result_text = f"Invalid command: {action.command}"
            reward.value -= 0.1
            reward.reason = "Invalid command penalty"
            
        if self.state_data.step_count >= self.state_data.max_steps and not self.state_data.is_done:
            self.state_data.is_done = True
            done = True
            reward.value = 0.0
            reward.reason = "Max steps reached"
            result_text = "Episode terminated due to max steps."
            
        current_knowledge = "\n".join(self.state_data.conversation_history + self.state_data.kb_queries + self.state_data.db_queries)
        
        obs = Observation(
            ticket_id=self.state_data.ticket_id,
            ticket_text=self.state_data.ticket_text,
            current_knowledge=current_knowledge,
            last_action_result=result_text,
            is_done=self.state_data.is_done
        )
        return obs, reward, done, info
        
    def state(self) -> State:
        return self.state_data
        
    def _current_obs(self) -> Observation:
        return Observation(
            ticket_id=self.state_data.ticket_id,
            ticket_text=self.state_data.ticket_text,
            current_knowledge="\n".join(self.state_data.conversation_history + self.state_data.kb_queries + self.state_data.db_queries),
            last_action_result="Episode is done.",
            is_done=self.state_data.is_done
        )
