import sys
from env import SupportTriageEnv, Action
from tasks.task1_basic_route import Task1BasicRoute
from tasks.task2_info_gathering import Task2InfoGathering
from tasks.task3_policy_resolution import Task3PolicyResolution
from tasks.task4_prompt_injection import Task4PromptInjection

def run_demo():
    print("=" * 60)
    print("   CUSTOMER SUPPORT TRIAGE - INTERACTIVE LIVE DEMO")
    print("=" * 60)
    
    tasks = [Task1BasicRoute(), Task2InfoGathering(), Task3PolicyResolution(), Task4PromptInjection()]
    env = SupportTriageEnv(tasks=tasks)
    
    print("\nSelect a Task to Play:")
    print("0 - Task 1 (Easy): Route a basic password reset request")
    print("1 - Task 2 (Medium): Gather missing app version before routing")
    print("2 - Task 3 (Hard): Deny an invalid refund based on policy OR approve if VIP")
    print("3 - Task 4 (Secret): Defend against prompt injection")
    
    task_idx = input("Enter task number (0, 1, 2, or 3): ").strip()
    try:
        task_idx = int(task_idx)
        if task_idx not in [0, 1, 2, 3]:
            raise ValueError
    except ValueError:
        print("Invalid selection. Defaulting to Task 0.")
        task_idx = 0
        
    obs, info = env.reset(task_idx=task_idx)
    done = False
    
    print("\n" + "="*40)
    print(f" NEW TICKET [{obs.ticket_id}]")
    print(f" Message: {obs.ticket_text}")
    print("="*40 + "\n")
    
    print("Available Commands:")
    print(" - ask_customer <your question>")
    print(" - search_kb <search query>")
    print(" - query_database <user_id or ticket_id>")
    print(" - route_ticket <department name>  (e.g., 'IT Support', 'Engineering')")
    print(" - resolve_ticket <resolution summary>  (e.g., 'Denied refund over 30 days')")
    print(" - quit (to exit demo)\n")
    
    while not done:
        user_input = input(">> Agent Action: ").strip()
        if not user_input:
            continue
            
        if user_input.lower() == 'quit':
            break
            
        parts = user_input.split(' ', 1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        action = Action(command=command, args=args)
        obs, reward, done, info = env.step(action)
        
        print(f"\n--- Environment Response ---")
        print(f"Result: {obs.last_action_result}")
        print(f"Reward Received: {reward.value:.2f}")
        print(f"Reason: {reward.reason}")
        print(f"----------------------------\n")
        
    print(f"Episode Completed! Final Score: {env.state().final_score:.2f} / 1.00")

if __name__ == "__main__":
    run_demo()
