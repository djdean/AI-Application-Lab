"""
TASK: Connect to Azure OpenAI using API Key Authentication

This script demonstrates a simpler (but less secure) authentication method:
- Uses hardcoded API key for direct connection (NOT recommended for production)
- Suitable for development, testing, and learning scenarios
- Implements an interactive chatbot with customizable behavior via system prompts
- Includes optional response assessment functionality

SECURITY WARNING ⚠️:
This approach stores credentials in code. For production applications:
1. Use environment variables: openai_key = os.getenv("AZURE_OPENAI_KEY")
2. Use managed identity: DefaultAzureCredential()
3. Never commit credentials to version control

Prerequisites:
1. Have an Azure OpenAI resource with a deployed model
2. Copy .env.example to .env
3. Fill in your endpoint, API key, and model name in .env
4. NEVER commit the .env file to git!
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main entry point - Sets up Azure OpenAI connection and runs interactive chat
    
    WORKSHOP TASK:
    1. Copy .env.example to .env
    2. Fill in AZURE_OPENAI_ENDPOINT with your endpoint from Azure Portal
    3. Fill in AZURE_OPENAI_API_KEY with your key (KEEP THIS SECRET!)
    4. Fill in AZURE_OPENAI_MODEL with your model deployment name
    5. Observe how system messages customize the AI behavior
    
    The script will:
    - Load credentials from .env file (more secure)
    - Connect to Azure OpenAI using API key auth
    - Accept user questions in a loop
    - Send each question to the model with a system prompt
    - The AI will respond in a sarcastic tone (due to system prompt)
    - Display the response
    """
    
    # STEP 1: Load configuration from environment variables
    print("Loading configuration from .env file...")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai_key = os.getenv("AZURE_OPENAI_API_KEY")
    model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")
    
    # STEP 2: Validate required environment variables
    if not endpoint:
        print("❌ ERROR: AZURE_OPENAI_ENDPOINT not found in environment variables")
        print("   Please copy .env.example to .env and fill in your endpoint")
        exit(1)
    if not openai_key:
        print("❌ ERROR: AZURE_OPENAI_API_KEY not found in environment variables")
        print("   Please copy .env.example to .env and fill in your API key")
        exit(1)
    
    print("Connecting to Azure OpenAI...")
    print(f"Endpoint: {endpoint}")
    print(f"Model: {model}\n")
    
    # STEP 3: Create OpenAI client with API key authentication
    # This uses direct API key authentication - simpler but less secure than managed identity
    # NOTE: We're loading the key from .env, which is much better than hardcoding it!
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=openai_key,
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


def assess_result(question, answer, client, model):
    """
    OPTIONAL WORKSHOP TASK: Assess whether an answer is complete
    
    This function demonstrates how to chain API calls - using one call result
    as input to another call. This is useful for:
    - Validating responses
    - Quality checking outputs
    - Multi-step reasoning workflows
    
    Parameters:
    - question: The original question asked
    - answer: The answer to assess
    - client: The OpenAI client
    - model: The model to use for assessment
    
    Returns:
    - "yes" or "no" indicating if the answer is complete
    """
    
    # Call the model to assess the answer
    # Notice the system prompt tells it to be proficient at assessment
    # This is an example of using prompts to give AI specific roles
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI assistant extremely proficient in assessing the confidence of answers coming from different users."},
            {"role": "user", "content": "\n\nBased on the following question: " + question + \
             "\n\nIs the following answer complete?\n\nAnswer:\n\n" + answer + "\n\n Respond yes or no."},
        ]
    )
    result = response.choices[0].message.content
    return result


def answer_question(question, client, model):
    """
    WORKSHOP TASK: Send a question to Azure OpenAI and get a response
    
    This function demonstrates the core API interaction pattern:
    1. Define the role and behavior with system messages
    2. Send the user's question as a user message
    3. Get the model's response
    4. Extract and return the content
    
    Parameters:
    - question: The user's question (string)
    - client: The OpenAI client
    - model: The model deployment name
    
    Returns:
    - Dictionary with 'content' key containing the model's response
    
    Key Concept - System Prompts:
    The "system" role sets the AI's personality and behavior.
    Here, it's instructed to be "sarcastic" - notice how this affects the response!
    """
    
    # Call the Azure OpenAI model with chat completion
    response = client.chat.completions.create(
        model=model,
        messages=[
            # SYSTEM PROMPT: Sets the AI's behavior and personality
            # This is like giving instructions to the AI about how to respond
            # WORKSHOP: Try changing this to test different behaviors!
            {"role": "system", "content": "You are an AI assistant extremely proficient in answering questions coming from different users. You are extremely sarcastic, please incorporate that into your responses."},
            # USER PROMPT: The actual question to answer
            {"role": "user", "content": "\n\nAnswer the following question:\n\n" + question},
        ]
    )
    
    # Extract the assistant's response from the API response object
    result = {
        "content": response.choices[0].message.content
    }
    return result
           
if __name__ == "__main__":
    main()

