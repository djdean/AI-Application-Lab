# Task 3: Complete Agent Communication Workflow

## Objective
Have a real conversation with an AI agent! You'll learn the complete workflow for:
1. **Starting a conversation** - Create a unique conversation thread
2. **Sending messages** - Ask the agent questions
3. **Processing responses** - Extract and display the agent's answers
4. **Checking history** - Retrieve all messages in the conversation
5. **Handling files** - Download charts or files the agent creates

This is the most complete and practical task—by the end, you'll have a working agent conversation!

## What You'll Learn
- How to create a conversation thread
- How to send messages and receive responses
- How to extract different types of content from responses
- How to view conversation history
- How to download files from the agent

## Prerequisites
✅ Completed **Task 1** (working Azure connection)
✅ Have an **agent ID** (from Task 2 or created in Azure portal)
✅ Your `.env` file must include the agent ID

## Step-by-Step Guide for Beginners

### IMPORTANT: Get Your Agent ID

**What you need to do:**
You need an agent ID to use in this task. Choose one:

**Option A: Use an agent from Task 2**
1. Run Task 2 again but don't delete the agent at the end
2. Save the agent ID when it's created

**Option B: Create an agent in Azure Portal**
1. Go to your Azure AI Foundry project
2. Create an agent there
3. Copy its agent ID

**Option C: Create one now**
1. Run `task_2_create_agent.py` but comment out the delete line at the end
2. Save the agent ID

**Add to .env file:**
```
AZURE_AI_FOUNDRY_ENDPOINT=your-endpoint-url
AZURE_AI_AGENT_ID=agent_xxxxx  (your agent ID)
```

### Step 1: Understand Threads (Conversations)

**Key concept:**
Each conversation with an agent needs a "thread":
- **Thread** = A container for all messages in one conversation
- **Message** = One turn in the conversation (user or agent)

**Real-world example:**
```
Thread 1: "How do I bake bread?"
├── User: "What ingredients do I need?"
├── Agent: "You need flour, water, salt..."
├── User: "How long to proof?"
└── Agent: "Usually 8-12 hours..."

Thread 2: "Python programming help"
├── User: "How do I read a file?"
├── Agent: "Use open() function..."
└── ...
```

Each thread keeps messages separate!

### Step 2: Look at SUB-TASK 1 - Start Conversation

**What happens in the code:**
```python
success = await client.start_conversation()  # Creates a new thread
if success:
    print(f"Thread ID: {client.thread_id}")  # You now have a conversation
```

**What to know:**
- `async` means this runs asynchronously (waits for Azure to respond)
- `await` pauses here until the thread is created
- `thread_id` is a unique ID for this conversation

**Why it matters:**
Without a thread, the agent doesn't know which conversation your message belongs to.

### Step 3: Look at SUB-TASK 2 - Send Message

**What happens:**
```python
response = await client.send_message("What is the capital of France?")
```

**Behind the scenes:**
1. Your message gets added to the thread
2. Azure creates a "run" (an execution of the agent)
3. The agent processes your message
4. You get back a response object

**The response object contains:**
- `message` - The text response from the agent
- `charts` - Any images or charts the agent created
- `error` - Any error that occurred

**Try different messages:**
```python
# Math question
await client.send_message("What is 25 * 16?")

# Python question
await client.send_message("Write me a Python function to reverse a string")

# Follow-up question (uses conversation context!)
await client.send_message("Can you explain that more simply?")
```

### Step 4: Look at SUB-TASK 3 - Process Response

**What happens:**
```python
response = await client.send_message(message)

if response.error:
    print(f"Error: {response.error}")  # Something went wrong
else:
    print(response.message)  # Display the agent's response
    if response.charts:
        print("Charts found: ", response.charts)  # Agent created files
```

**Processing includes:**
- ✅ Extracting text from the response
- ✅ Finding any images or charts
- ✅ Handling different content types
- ✅ Detecting errors

### Step 5: Look at SUB-TASK 4 - Get Conversation History

**What happens:**
```python
history = await client.get_conversation_history()
# Returns all messages in the current thread
for message in history:
    print(f"{message.role}: {message.content}")  # Show who said what
```

**Example output:**
```
User: What is the capital of France?
Agent: The capital of France is Paris.
User: What's its population?
Agent: Paris has approximately 2.1 million people.
```

**Why this matters:**
- Shows the complete conversation flow
- Useful for logging and auditing
- Helps you understand the conversation context

### Step 6: Look at SUB-TASK 5 - Handle Files (Optional)

**What happens:**
If the agent creates files (charts, documents, etc.), you can download them:

```python
if response.charts:
    for chart in response.charts:
        file_id = chart['file_id']
        filename = chart['filename']
        # Download the file
        await client.download_file(file_id, filename)
        print(f"✅ Saved {filename}")
```

**When this happens:**
- Agent creates a data visualization
- Agent generates a report
- Agent produces any file output

## Step-by-Step Execution

### Setup

1. Make sure your `.env` file has:
   ```
   AZURE_AI_FOUNDRY_ENDPOINT=your-endpoint-url
   AZURE_AI_AGENT_ID=agent_xxxxx
   ```

2. Open `task_3_agent_communication.py`

3. (Optional) Modify the message to test:
   ```python
   # Change this line to test different queries
   message = "Write me a Python function to calculate factorial"
   ```

### Running the Script

1. Open terminal in VS Code
2. Navigate to the task directory:
   ```
   cd "Day 3\Hands on Tasks\3.InteractWithAIAgents"
   ```
3. Run the script:
   ```
   python task_3_agent_communication.py
   ```

### What You Should See

**Expected output:**
```
============================================================
SUB-TASK 1: Start Conversation
============================================================
Creating a new conversation thread with the agent...

✅ Conversation started successfully!
   Thread ID: thread_abc123def456
   This ID uniquely identifies your conversation

============================================================
SUB-TASK 2: Send Message to Agent
============================================================
Sending message: 'What is the capital of France?'

✅ Message sent successfully!

============================================================
SUB-TASK 3: Process Response
============================================================
Agent Response:
"The capital of France is Paris, the largest city..."

============================================================
SUB-TASK 4: Get Conversation History
============================================================
Conversation History:
─────────────────────────────────
User: What is the capital of France?
Agent: The capital of France is Paris...
─────────────────────────────────
```

### Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `Agent ID not found` | Missing AZURE_AI_AGENT_ID in .env | Add agent ID to .env file |
| `Failed to start conversation` | Agent doesn't exist | Create agent in Task 2 or portal |
| `Failed to send message` | Agent not deployed | Check agent status in Azure portal |
| `No response from assistant` | Agent took too long | Try again, or check agent configuration |

## Advanced: Multi-Turn Conversation

**For advanced learners:**
Modify the script to have a multi-turn conversation:

```python
async def main():
    # ... setup code ...
    
    # First message
    response1 = await client.send_message("What is 2+2?")
    print(response1.message)
    
    # Second message (uses conversation context!)
    response2 = await client.send_message("What about 3+3?")
    print(response2.message)
    
    # Get full history
    history = await client.get_conversation_history()
    for msg in history:
        print(f"{msg.role}: {msg.content}")
```

## Summary

**What you accomplished:**
✅ Created a conversation thread  
✅ Sent messages to an AI agent  
✅ Received and processed responses  
✅ Retrieved conversation history  
✅ Learned how to handle files (optional)  

**Key skills:**
- Understanding how agents maintain conversation context
- Processing different types of agent responses
- Retrieving and viewing conversation history
- Handling agent-generated files

**You now know:**
- 🎯 How to initialize and connect to Azure AI
- 🎯 How to create agents programmatically
- 🎯 How to have complete conversations with agents

**Congratulations!** You've mastered the fundamentals of Azure AI agent development! 🎉
