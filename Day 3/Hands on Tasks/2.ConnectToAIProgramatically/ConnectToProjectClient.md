# Connect to Project Client

## Overview
This script demonstrates how to programmatically connect to Azure AI resources using the **Azure AI Projects SDK**. It uses Azure's managed identity authentication to securely access an Azure OpenAI deployment without storing API keys in your code.

This is a beginner-friendly introduction to using Azure's modern Python SDK for AI applications, which is the recommended approach for production environments.

## What This Script Does
- **Authenticates** to Azure using `DefaultAzureCredential()` (managed identity)
- **Connects** to an Azure AI Project endpoint
- **Initializes** an OpenAI client from the project
- **Creates an interactive chatbot** that accepts questions and returns answers from the AI model
- Uses the OpenAI chat API format to send prompts and receive responses

## Key Concepts
- **DefaultAzureCredential**: Automatically finds the right authentication method (no hardcoded keys)
- **AIProjectClient**: SDK for managing Azure AI Projects
- **OpenAI Client**: Used to interact with the language model

## Step-by-Step Implementation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
This installs the required packages:
- `openai` - OpenAI SDK for Python
- `azure-identity` - Azure authentication
- `azure-ai-projects` - Azure AI Projects SDK

### Step 2: Set Your Endpoint
- Replace the placeholder endpoint URL with your actual Azure AI Project endpoint
- Location in code: The `endpoint` parameter in `AIProjectClient()`
- Format: `https://<your-resource>.services.ai.azure.com/api/projects/<project-id>`

### Step 3: Verify Azure Authentication
- Ensure you're logged in to Azure locally using Azure CLI:
  ```bash
  az login
  ```
- Or set appropriate environment variables for your authentication method
- `DefaultAzureCredential` will automatically use your local Azure credentials

### Step 4: Set Your Model Name
- Replace `"gpt-5.2-chat"` with your actual model deployment name
- This should match the model name in your Azure AI Project

### Step 5: Run the Script
```bash
python ConnectToProjectClient.py
```

### Step 6: Interact with the Chatbot
- Enter your questions at the prompt
- The script will send them to the AI model and display the response
- Type `exit` to quit the program

## Important Notes
- ✅ **Security Best Practice**: No API keys are hardcoded in the script
- ✅ **Production Ready**: Uses managed identity authentication
- ⚠️ **Endpoint & Model**: Customize these for your environment
- ⚠️ **Response Format**: The response parsing uses `response.output_text` - verify this matches your SDK version
