# Customer Support Triage OpenEnv

This is a real-world task environment for evaluating AI agents on their ability to handle customer support tickets. The agent must gather missing information, consult return policies, and route or resolve tickets accurately.

## Motivation & Real-world Utility (30% Criteria)
Customer support is a ubiquitous, complex real-world task that involves reasoning, information gathering, policy adherence, and proper judgment. Rather than toy grid-worlds, this environment tests an LLM's ability to act as a frontline support agent, deciding whether to route tickets to human departments or resolve them locally based on retrieved knowledge.

## Observation & Action Space

### Observation
- `ticket_id`: The ID of the support ticket.
- `ticket_text`: The initial message from the customer.
- `current_knowledge`: A string containing the history of the conversation and KB search results.
- `last_action_result`: The string response of the environment to the last action taken.
- `is_done`: Boolean indicating if the episode has terminated.

### Action
- `command`: One of `ask_customer`, `search_kb`, `route_ticket`, `resolve_ticket`.
- `args`: Command-specific arguments (e.g., questions, search queries, department routing choices, resolution strings).

## Tasks (25% Criteria)
1. **Easy (Task 1):** Explicit routing request (Password Reset to IT Support).
2. **Medium (Task 2):** Information gathering (Asking for App Version for Bug Reports before routing to Engineering).
3. **Hard (Task 3):** Policy enforcement (Recognizing an invalid refund request out of the 30-day window and denying it).

## Setup Instructions

### Local Installation
```bash
cd support_triage_env
pip install -e .
```

### Environment Execution
Start the environment as an OpenEnv FastAPI server:
```bash
openenv serve env:SupportTriageEnv --port 7860
```

### Running Baseline Inference
You can run the baseline inference script using the standard OpenAI client.
```bash
export OPENAI_API_KEY="your_key"
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o"
python Inference.py
```

## Docker (15% Criteria)
```bash
docker build -t support_triage_env .
docker run -p 7860:7860 support_triage_env
```
