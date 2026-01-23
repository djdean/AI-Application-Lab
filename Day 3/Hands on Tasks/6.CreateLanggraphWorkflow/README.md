# Create a LangGraph Workflow - Quick Start Guide

## What You'll Build
- A minimal LangGraph that routes user turns to an Azure AI Foundry Agent
- A CLI loop to chat with the graph
- Optional extension task to add a summarizer node

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the environment template and fill your values:
   ```bash
   cp .env.example .env
   ```
3. Provide your Azure settings in `.env` (endpoint, agent ID, and either API key or DefaultAzureCredential values).
4. Run the first workflow:
   ```bash
   python task_1_workflow.py
   ```

## Files
- [overview.md](Create%20Langgraph%20Workflow/overview.md)
- [task_1.md](Create%20Langgraph%20Workflow/task_1.md)
- [task_2.md](Create%20Langgraph%20Workflow/task_2.md)
- [task_1_workflow.py](Create%20Langgraph%20Workflow/task_1_workflow.py)
- [requirements.txt](Create%20Langgraph%20Workflow/requirements.txt)
- [.env.example](Create%20Langgraph%20Workflow/.env.example)

## Workshop Flow
1. Read the overview, then configure your environment variables.
2. Complete Task 1 to run the single-node LangGraph that calls your Azure AI Foundry Agent.
3. (Optional) Follow Task 2 to extend the graph with a summarizer node.
4. Consider wiring the graph into Streamlit or FastAPI once the basics work.

## Troubleshooting
- Missing env vars: ensure `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_AGENT_ID` are set.
- Auth errors: use `AZURE_OPENAI_API_KEY` or set `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET` for DefaultAzureCredential.
- Slow runs: increase `timeout` or decrease `poll_interval` inside the workflow.
