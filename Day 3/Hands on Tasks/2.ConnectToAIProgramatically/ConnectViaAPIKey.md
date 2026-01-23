# Connect Via API Key

## Overview
This script demonstrates how to connect to Azure OpenAI using an **API Key** for authentication. This is a simpler authentication method than managed identity and is useful for development, testing, and learning scenarios.

It includes interactive question-answering capabilities and demonstrates how to structure prompts to get sarcastic responses from the AI.

## What This Script Does
- **Authenticates** to Azure OpenAI using an API key
- **Sends prompts** to the AI model with system messages to set behavior
- **Creates an interactive chatbot** that asks for questions and returns answers
- **Includes an assessment function** that can evaluate answer completeness (optional)
- Demonstrates system prompts to customize AI behavior (in this case, making it sarcastic)

## Key Concepts
- **API Key Authentication**: Direct credential using an API key string
- **System Messages**: Instructions to the AI about how to behave
- **User Messages**: The actual prompts/questions for the AI
- **Chat Completion API**: OpenAI's API for question-answering conversations

## Security Warning ⚠️
**This approach stores the API key in the code**, which is NOT recommended for production. For this workshop, it's acceptable for learning purposes, but production code should use environment variables or `DefaultAzureCredential()`.

## Step-by-Step Implementation

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
This installs the required packages:
- `openai` - OpenAI SDK for Python
- `azure-identity` - Azure authentication (if using bearer token method instead)

### Step 2: Set Your Endpoint
- Replace `"https://sweden-central-aoai-dade.openai.azure.com/openai/v1"` with your Azure OpenAI endpoint
- Format: `https://<your-resource>.openai.azure.com/openai/v1`
- This is typically found in your Azure OpenAI resource's "Keys and Endpoint" page

### Step 3: Set Your API Key
- Replace `"17a0c23410f04fc09d3037b1972e3e5e"` with your actual API key
- **IMPORTANT**: Never commit keys to version control in real projects
- In production, store this in environment variables:
  ```python
  import os
  openai_key = os.getenv("AZURE_OPENAI_KEY")
  ```

### Step 4: Set Your Model Name
- Replace `"gpt-5.2-chat"` with your actual model deployment name
- This must match the deployment name in your Azure OpenAI resource

### Step 5: Run the Script
```bash
python ConnectViaAPIKey.py
```

### Step 6: Interact with the Chatbot
- Enter your questions at the prompt
- The AI will respond with answers (in a sarcastic tone due to the system prompt)
- Type `exit` to quit the program

### Step 7: (Optional) Test the Assessment Function
- The `assess_result()` function is defined but not called in the main loop
- You can modify the script to use it if you want to evaluate answer quality:
  ```python
  answer = answer_question(question, client, model)
  assessment = assess_result(question, answer["content"], client, model)
  print("Assessment:", assessment)
  ```

## Important Notes
- ⚠️ **Security Risk**: API key is stored in code - use environment variables instead
- ✅ **Simple Setup**: Easy to get started with minimal dependencies
- ⚠️ **No Managed Identity**: Requires manual key management
- 📝 **Customizable Behavior**: System prompt can be modified to change AI behavior
- 📝 **Sarcasm Prompt**: Current system prompt makes the AI respond sarcastically - change this for different behavior
