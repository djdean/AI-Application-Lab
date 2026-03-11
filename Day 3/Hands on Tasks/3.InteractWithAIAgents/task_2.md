# Task 2: Create an Agent Programmatically

## Objective
Create and manage AI agents using Python code instead of the Azure portal. You'll create an agent, retrieve its details, and clean it up when done. This teaches you how to automate agent creation in real applications.

## What You'll Learn
- How to create agents with custom instructions
- How to retrieve agent information
- How to clean up resources by deleting agents
- Why agent configuration matters

## Prerequisites
✅ You must have completed **Task 1** first (working Azure connection)
✅ Your `.env` file is properly configured

## Step-by-Step Guide for Beginners

### Step 1: Understand What an Agent Is

**Simple explanation:**
An "agent" is an AI that you've configured with:
- **Model:** The AI engine (like gpt-4o)
- **Name:** A descriptive identifier
- **Instructions:** A system prompt that tells the AI how to behave
- **Tools:** Optional functions the AI can call (not used in this task)

**Example:** You might create an agent that says "You are a customer service expert" in its instructions. That same model could create a different agent with "You are a Python coding expert."

### Step 2: Review the Configuration

**What you need to do:**
1. Open `task_2_create_agent.py`
2. Look at the `load_configuration()` function (around line 40)

**What it does:**
```python
endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")  # From your .env file
model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")  # Model to use (default: gpt-4o)
```

**Key point:** The default model is `gpt-4o`. If you deployed a different model in Azure, update your `.env` file:
```
AZURE_OPENAI_MODEL=your-model-name
```

### Step 3: Look at SUB-TASK 1 - Create Agent

**What happens:**
The `subtask_1_create_agent()` function creates a new agent with:

```python
model="gpt-4o"                 # The AI engine
name="workshop-agent"          # A name for this agent
instructions="You are a helpful AI assistant..."  # How it should behave
```

**Important:** The instructions are crucial! They tell the AI:
- How to speak (formal? casual?)
- What topics to focus on
- What boundaries to respect
- What style of response to use

**Try modifying the instructions:**
Change the instructions to test different behaviors:
```python
# Option 1: Make it a Python expert
instructions="You are an expert Python programmer. Provide code examples and explain concepts simply."

# Option 2: Make it formal
instructions="You are a professional business consultant. Provide detailed, formal responses."
```

### Step 4: Look at SUB-TASK 2 - Retrieve Agent Details

**What happens:**
After creating the agent, we fetch its details to verify it was created:

```python
agent = await client.get_agent(agent_id)  # Get the agent we just created
print(agent.name)       # Shows the agent's name
print(agent.model)      # Shows which model it uses
print(agent.instructions)  # Shows the system instructions
```

**Why this matters:** Retrieving verifies that the creation worked and shows you what the agent looks like.

### Step 5: Look at SUB-TASK 3 - Delete Agent (Resource Cleanup)

**What you need to know:**
In the full code (scroll down), there's a cleanup section that deletes the agent:

```python
await client.delete_agent(agent_id)  # Remove the agent
```

**Why this matters:** 
- Agents consume Azure resources
- Always clean up when you're done testing
- In production, save the agent ID for later use instead of deleting

## Step-by-Step Execution

### Prerequisites Check
1. Open `task_2_create_agent.py`
2. Make sure your `.env` file has:
   ```
   AZURE_AI_FOUNDRY_ENDPOINT=your-endpoint-url
   AZURE_OPENAI_MODEL=gpt-4o  # (or whatever model you deployed)
   ```

### Running the Script

**What to do:**
1. Open the terminal in VS Code
2. Navigate to the task directory:
   ```
   cd "Day 3\Hands on Tasks\3.InteractWithAIAgents"
   ```
3. Run the script:
   ```
   python task_2_create_agent.py
   ```

**What you should see:**
```
============================================================
SUB-TASK 1: Create Agent
============================================================
Creating a new agent with the following configuration:
  - Model: gpt-4o
  - Name: workshop-agent
  - Instructions: You are a helpful AI assistant...

✅ Agent created successfully!
   Agent ID: agent_12345678 (this ID is unique to your agent)

============================================================
SUB-TASK 2: Retrieve Agent Details
============================================================
✅ Agent retrieved successfully!
   Name: workshop-agent
   Model: gpt-4o
   Instructions: You are a helpful AI assistant...
   Status: Active and ready to use

============================================================
SUB-TASK 3: Delete Agent
============================================================
✅ Agent deleted successfully!
```

### Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Failed to create agent` | Model not deployed | Check your AZURE_OPENAI_MODEL in .env |
| `Agent ID is None` | Authentication failed | Run `az login` and check .env |
| `PermissionError` | Don't have rights to deploy models | Contact your Azure admin |

### (Optional) Challenge: Experiment with Instructions

**For advanced learners:**
1. Modify the instructions in the code
2. Create multiple agents with different instructions
3. Note the agent IDs
4. Later in Task 3, test how different instructions affect responses

**Example variations:**
- "You are a helpful assistant that responds in bullet points"
- "You are an expert data scientist who explains concepts with examples"
- "You are a pirate who provides helpful information in pirate speak"

## Summary

**What you accomplished:**
✅ Understood what agents are and how they're configured  
✅ Successfully created an AI agent with custom instructions  
✅ Retrieved and verified the agent's details  
✅ Cleaned up resources by deleting the agent  

**Key concept:** Creating agents programmatically lets you automate agent deployment in real applications.

**Next step:** Task 3 - Use the agent you created (or create a new one and save its ID) to have actual conversations!
