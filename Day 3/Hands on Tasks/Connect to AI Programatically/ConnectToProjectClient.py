"""
TASK: Connect to Azure AI Project using Managed Identity (DefaultAzureCredential)

This script demonstrates the recommended way to authenticate to Azure AI services:
- Uses managed identity/DefaultAzureCredential (no hardcoded credentials)
- Creates a secure project client connection to Azure AI Foundry
- Implements an interactive chatbot for Q&A with the deployed model

Prerequisites:
1. Copy .env.example to .env and fill in your values
2. Ensure you're logged in to Azure (az login) or have proper Azure credentials
3. Set your endpoint and model in the .env file
"""

import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main entry point - Sets up Azure AI connection and runs interactive chat loop
    
    WORKSHOP TASK:
    1. Copy .env.example to .env
    2. Fill in AI_FOUNDRY_ENDPOINT with your endpoint from Azure Portal
    3. Fill in AZURE_OPENAI_MODEL with your deployed model name
    4. Verify you can authenticate using DefaultAzureCredential (run 'az login')
    
    The script will:
    - Load configuration from .env file
    - Connect to your Azure AI project
    - Get an OpenAI-compatible client
    - Accept user questions in a loop
    - Send each question to the AI model
    - Display the model's response
    """
    
    # STEP 1: Load configuration from environment variables
    # These are loaded from the .env file (never commit .env to git!)
    endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
    model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4.1-mini")  # Default to gpt-4.1-mini if not set
    
    # Validate required environment variables
    if not endpoint:
        print("❌ ERROR: AZURE_AI_FOUNDRY_ENDPOINT not found in environment variables")
        print("   Please copy .env.example to .env and fill in your endpoint")
        exit(1)
    
    # STEP 2: Create Azure AI Project client using managed identity authentication
    # DefaultAzureCredential automatically finds the right auth method:
    #   - Environment variables
    #   - Managed identity (if in Azure)
    #   - Azure CLI credentials (if locally logged in with 'az login')
    #   - Other fallback methods
    # This is more secure than storing API keys in code
    print(f"Connecting to: {endpoint}")
    print(f"Using model: {model}\n")
    
    project = AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    )
    
    # STEP 3: Get an OpenAI-compatible client from the project
    # This client can be used to call the deployed model using standard OpenAI API
    openai_client = project.get_openai_client()
    
    # STEP 4: Interactive loop - accept user questions until 'exit'
    question = ""
    while True:
        # Get user input
        question = input("\nEnter a question to ask " + model + " or 'exit' to quit:\n")
        
        # Check for exit command
        if question == "exit":
            exit(0)
        
        # Send question to model and get answer
        answer = answer_question(question, openai_client, model)
        print("Answer:\n\n" + answer["content"] + "\n\n")


def answer_question(question, client, model):
    """
    WORKSHOP TASK: Send a question to the Azure AI model and get a response
    
    Parameters:
    - question: The user's question (string)
    - client: The OpenAI-compatible client from the project
    - model: The model deployment name
    
    Returns:
    - Dictionary with 'content' key containing the model's response
    
    Process:
    1. Format the question as input to the model
    2. Call the model using the OpenAI SDK
    3. Extract the response
    4. Return as a dictionary
    """
    
    # Call the Azure AI model with the question
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

