# Task 1: Build a Single-Node LangGraph with an Azure AI Foundry Agent

## Objective
Create a LangGraph with one node that forwards user input to an Azure AI Foundry Agent and returns the assistant reply via a simple CLI loop.

## Learning Goals
- Define LangGraph state and nodes
- Call an Azure AI Foundry Agent from Python
- Manage a thread to keep conversation continuity
- Run and observe the graph in a CLI

## Steps

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Configure environment variables
Copy the template and set your values:
```bash
cp .env.example .env
```
Fill in:
- `AZURE_OPENAI_ENDPOINT`: your Azure AI Foundry endpoint
- `AZURE_OPENAI_AGENT_ID`: the Agent ID you want to run
- Authentication:
  - `AZURE_OPENAI_API_KEY` **or**
  - `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` for DefaultAzureCredential

### 3) Review the workflow code
Open [task_1_workflow.py](Create%20Langgraph%20Workflow/task_1_workflow.py). Key pieces:
- `ChatState`: keeps message history and the agent thread ID
- `call_agent`: adds the latest user turn to the thread, runs the agent, polls, and captures the newest assistant reply
- Graph: a single node `agent_turn` wired to `END`
- CLI loop: appends user input to history, invokes the graph, and prints the reply

### 4) Run the graph
From this folder:
```bash
python task_1_workflow.py
```
Try a prompt like "Plan a 3-step checklist for brewing coffee". Type `exit` or `quit` to stop.

## Expected Behavior
- First run creates a thread, sends your user message, polls the run, and prints the assistant response
- Subsequent turns reuse the same thread ID to keep context

## Troubleshooting
- Missing environment vars: set `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_AGENT_ID`
- Auth failures: provide `AZURE_OPENAI_API_KEY` or the Azure AD client credentials
- No reply: ensure the Agent is deployed and the model is available; increase `timeout` if needed

## Challenge
- Add basic retry logic around `call_agent`
- Log each turn to a file for later review
