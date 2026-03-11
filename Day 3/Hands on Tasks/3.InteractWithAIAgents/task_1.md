# Task 1: Creating the Azure AI Client

## Objective
Establish a working connection to Azure AI Foundry services by creating and configuring the AzureAIFoundryClient. This is the foundation for all other tasks—you need a working client before you can create or interact with agents.

## What You'll Learn
- How to load configuration from environment variables
- How to instantiate the Azure AI Foundry client
- How to validate that your connection is working
- How to handle configuration errors

## Step-by-Step Guide for Beginners

### Step 1: Prepare Your Environment Configuration

**What you need to do:**
- Create a `.env` file in the same directory as your Python script (if it doesn't exist)
- Add your Azure AI Foundry endpoint URL to this file

**How to do it:**
1. Open File Explorer and navigate to: `Day 3/Hands on Tasks/3.InteractWithAIAgents/`
2. Create a new file named `.env` (note the dot at the beginning)
3. Open `.env.example` to see what format to use
4. Copy the format and add your actual endpoint:
   ```
   AZURE_AI_FOUNDRY_ENDPOINT=https://your-endpoint.api.azureml.ms
   ```
5. Save the file

**Why this matters:** Your Azure credentials are sensitive, so we store them in a `.env` file that never gets committed to version control.

### Step 2: Understand the Configuration Class

**What you need to know:**
The `AzureAIConfig` class is a simple data container that holds your connection settings:
```python
@dataclass
class AzureAIConfig:
    endpoint: str              # Your Azure AI Foundry URL
    agent_id: Optional[str] = None  # (Optional for Task 1)
```

**In `task_1_create_client.py`:** Look at the `load_configuration()` function. It:
1. Reads the endpoint from your `.env` file
2. Validates that the endpoint exists
3. Creates an `AzureAIConfig` object with that endpoint

### Step 3: Understand Azure Authentication

**What you need to know:**
`DefaultAzureCredential` is Azure's way of securely finding your credentials. It tries multiple methods in order:
1. Environment variables (if set)
2. Managed identity (if running in Azure)
3. Azure CLI (if you've run `az login`)
4. Visual Studio credentials
5. Azure PowerShell credentials

**In the code:** Line with `credential = DefaultAzureCredential()` uses whatever authentication method is available on your system.

### Step 4: Create the Client

**What happens:**
The `create_client()` function creates the actual connection to Azure:

```python
1. credential = DefaultAzureCredential()  # Get your credentials
2. client = AzureAIFoundryClient(config, credential=credential)  # Connect to Azure
3. if client.client:  # Check if connection succeeded
   print("✅ Success!")  # Connection works!
```

**What to watch for:**
- ❌ If you see "Client not created", your credentials aren't set up correctly
- ✅ If you see "Client created successfully!", you're ready for Task 2

### Step 5: Test the Connection

**What you need to do:**
1. Open `task_1_create_client.py` in Visual Studio Code
2. In the terminal, run:
   ```
   python task_1_create_client.py
   ```
3. Look at the output:
   - If you see `✅ Azure AI client created successfully!` → Success! ✅
   - If you see errors → Check your `.env` file and credentials

**Troubleshooting:**

| Error | What It Means | How to Fix |
|-------|---------------|----------|
| AZURE_AI_FOUNDRY_ENDPOINT not found | Your `.env` file is missing or has the wrong variable name | Create/update `.env` file with the correct endpoint |
| Failed to create client | Your credentials aren't set up | Run `az login` in terminal to set up Azure CLI credentials |
| Connection timeout | Can't reach Azure | Check your internet connection and firewall |

## Summary

**What you accomplished:**
✅ Created a `.env` configuration file  
✅ Learned about the `AzureAIConfig` class  
✅ Understood Azure authentication methods  
✅ Successfully connected to Azure AI Foundry  

**Next step:** Move on to Task 2 to create your first agent!
