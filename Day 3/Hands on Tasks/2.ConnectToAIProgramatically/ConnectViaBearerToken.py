"""
TASK: Connect to Azure OpenAI using Bearer Token Authentication

This script demonstrates a secure, modern authentication method:
- Uses DefaultAzureCredential to automatically obtain bearer tokens
- Tokens are generated dynamically without storing credentials in code
- More secure than API keys, simpler than full project-based authentication
- Implements an interactive chatbot for Q&A

Authentication Flow:
1. DefaultAzureCredential finds your Azure credentials from:
   - Environment variables
   - Managed identity (if running in Azure)
   - Azure CLI credentials (if you've run 'az login')
   - Other Azure auth methods
2. Creates a token provider that generates fresh tokens on demand
3. OpenAI client uses tokens instead of hardcoded keys

Prerequisites:
1. Run 'az login' to authenticate with Azure CLI
2. Copy .env.example to .env
3. Fill in your endpoint and model name in .env
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main entry point - Sets up Azure OpenAI with bearer token auth and runs chat
    
    WORKSHOP TASK:
    1. Verify you're logged in: run 'az login' in your terminal
    2. Copy .env.example to .env
    3. Fill in AZURE_OPENAI_ENDPOINT in .env
    4. Fill in AZURE_OPENAI_MODEL in .env
    5. Note: No API keys needed - much more secure!
    
    The script will:
    - Load configuration from .env file
    - Create a token provider using managed identity
    - Connect to Azure OpenAI with dynamic tokens
    - Accept user questions in a loop
    - Send each question to the model
    - Display the response
    """
    
    # STEP 1: Load configuration from environment variables
    print("Loading configuration from .env file...")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")
    
    # Validate required environment variables
    if not endpoint:
        print("❌ ERROR: AZURE_OPENAI_ENDPOINT not found in environment variables")
        print("   Please copy .env.example to .env and fill in your endpoint")
        exit(1)
    
    print(f"Endpoint: {endpoint}")
    print(f"Model: {model}")
    print("Creating bearer token provider...")
    
    # STEP 2: Create a bearer token provider using DefaultAzureCredential
    # This is the key advantage of this approach:
    # - No hardcoded credentials
    # - Tokens are generated automatically and refreshed as needed
    # - Supports multiple auth methods (CLI, managed identity, env vars, etc.)
    # The "https://cognitiveservices.azure.com/.default" scope tells Azure
    # which service this token is for (Azure Cognitive Services)
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default"
    )

    # STEP 3: Create OpenAI client using bearer token authentication
    # Instead of an API key, we pass the token_provider
    # This client will automatically use fresh tokens
    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider,
    )
    print("✅ Connected successfully!\n")
    
    # STEP 4: Interactive loop - accept user questions until 'exit'
    question = ""
    while True:
        # Get user input
        question = input("\nEnter a question to ask " + model + " or 'exit' to quit:\n")
        
        # Check for exit command
        if question == "exit":
            exit(0)
        
        # Send question to model and get answer
        answer = answer_question(question, client, model)
        print("Answer:\n\n" + answer["content"] + "\n\n")


def answer_question(question, client, model):
    """
    WORKSHOP TASK: Send a question to the Azure OpenAI model and get a response
    
    This function demonstrates the core API interaction with bearer token auth.
    The key difference from API key auth is that tokens are managed automatically
    by the token_provider, keeping your code secure.
    
    Parameters:
    - question: The user's question (string)
    - client: The OpenAI client (configured with bearer token provider)
    - model: The model deployment name
    
    Returns:
    - Dictionary with 'content' key containing the model's response
    """
    
    # Call the Azure OpenAI model with the question
    response = client.responses.create(
        model=model,
        input="question: " + question,
    )
    
    # Extract the response text and return as dictionary
    result = {
        "content": response.output_text
    }
    return result
           
if __name__ == "__main__":
    main()

