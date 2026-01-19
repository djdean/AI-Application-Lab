# Connect Via Bearer Token

## Overview
This script demonstrates how to connect to Azure OpenAI using **Bearer Token** authentication with Azure managed identity. This approach uses `DefaultAzureCredential` to automatically obtain a bearer token, providing a secure, modern authentication method without storing API keys in code.

This is a middle-ground approach that's more secure than API keys but simpler than full project-based authentication.

## What This Script Does
- **Authenticates** to Azure using a bearer token provider from `DefaultAzureCredential`
- **Generates tokens** dynamically without storing credentials
- **Connects** to Azure OpenAI using the OpenAI SDK with token-based auth
- **Creates an interactive chatbot** that accepts questions and returns answers
- Uses Azure's identity system for automatic credential management

## Key Concepts
- **Bearer Token Provider**: Automatically generates fresh tokens for authentication
- **DefaultAzureCredential**: Finds the appropriate authentication method from your environment
- **Token-Based Auth**: More secure than API keys, no hardcoded secrets
- **Azure Cognitive Services Scope**: Uses the default Azure Cognitive Services scope for authorization

## Step-by-Step Implementation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
This installs the required packages:
- `openai` - OpenAI SDK for Python
- `azure-identity` - Azure authentication and token management

### Step 2: Verify Azure Authentication
- Ensure you're logged in to Azure locally:
  ```bash
  az login
  ```
- Or set appropriate environment variables for your authentication method:
  - `AZURE_SUBSCRIPTION_ID`
  - `AZURE_TENANT_ID`
  - `AZURE_CLIENT_ID` and `AZURE_CLIENT_SECRET` (for service principals)
- `DefaultAzureCredential` will automatically use your credentials in this order:
  1. Environment variables
  2. Managed identity (if running in Azure)
  3. Azure CLI credentials (if logged in)
  4. Visual Studio Code extension credentials
  5. Azure PowerShell credentials

### Step 3: Set Your Endpoint
- Replace `"https://AIWorkshopTest.openai.azure.com/openai/v1/"` with your Azure OpenAI endpoint
- Format: `https://<your-resource>.openai.azure.com/openai/v1/`
- This is found in your Azure OpenAI resource's "Keys and Endpoint" page

### Step 4: Set Your Model Name
- Replace `"gpt-5.2-chat"` with your actual model deployment name
- This must match the deployment name in your Azure OpenAI resource

### Step 5: Run the Script
```bash
python ConnectViaBearerToken.py
```

### Step 6: Interact with the Chatbot
- Enter your questions at the prompt
- The script will send them to the AI model and display the response
- Type `exit` to quit the program

## How Bearer Token Authentication Works
```python
# This creates a function that generates fresh bearer tokens
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), 
    "https://cognitiveservices.azure.com/.default"
)

# The OpenAI client uses this function to get tokens automatically
client = OpenAI(
    base_url = "https://your-resource.openai.azure.com/openai/v1/",
    api_key=token_provider  # Actually a token provider, not a static key
)
```

## Important Notes
- ✅ **Security Best Practice**: No static API keys in code
- ✅ **Automatic Token Management**: Tokens are generated and refreshed automatically
- ✅ **Flexible Authentication**: Works with multiple Azure auth methods
- ⚠️ **Azure Login Required**: You must be authenticated to Azure (via `az login` or environment variables)
- ⚠️ **Endpoint & Model**: Customize these for your environment
- 🔄 **Token Refresh**: Tokens are automatically refreshed when they expire
