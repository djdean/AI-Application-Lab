"""
TASK 1: Creating the Azure AI Client

Objective:
Implement the AzureAIFoundryClient class to establish a connection with 
Azure AI Foundry services. This is the first step in building an AI agent 
application - you need a working client before you can create or interact 
with agents.

Learning Goals:
- Understand how to instantiate an Azure AI client
- Learn error handling for connection issues
- Practice configuring authentication with Azure credentials
- Verify your connection to Azure AI services

What You'll Do:
1. Create an AzureAIConfig object with your Azure AI endpoint
2. Instantiate the AzureAIFoundryClient with that config
3. Handle any exceptions that might occur
4. Test the connection

Why This Matters:
The client is the gateway to all Azure AI operations. A successful client
connection means your authentication is working and you can proceed to
create agents, threads, and messages.
"""

import os
from dotenv import load_dotenv
from azure_client import AzureAIFoundryClient, AzureAIConfig
from azure.identity import DefaultAzureCredential

# Load environment variables from .env file
load_dotenv()


def load_configuration():
    """
    SUB-TASK 1: Load configuration from environment variables.
    
    Returns:
        tuple: (endpoint, config) or (None, None) if validation fails
    """
    print("="*60)
    print("SUB-TASK 1: Load Configuration")
    print("="*60)
    
    # Load configuration from environment variables
    endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
    
    # Validate required environment variables
    if not endpoint:
        print("❌ AZURE_AI_FOUNDRY_ENDPOINT not found in environment variables")
        print("   Please copy .env.example to .env and fill in your endpoint")
        return None, None
    
    print(f"Loading configuration...")
    print(f"Endpoint: {endpoint}")
    print()
    
    # Create an AzureAIConfig object
    config = AzureAIConfig(
        endpoint=endpoint,
        agent_id="placeholder"
    )
    
    return endpoint, config


def create_client(config):
    """
    SUB-TASK 2: Create the Azure AI Foundry client.
    
    Args:
        config: AzureAIConfig object with endpoint configuration
        
    Returns:
        AzureAIFoundryClient or None if creation fails
    """
    print("="*60)
    print("SUB-TASK 2: Create Azure AI Client")
    print("="*60)
    
    # Initialize Azure credentials
    # DefaultAzureCredential automatically tries multiple authentication methods:
    # 1. Environment variables
    # 2. Managed identity (if running in Azure)
    # 3. Azure CLI credentials (if you've run 'az login')
    # 4. Visual Studio credentials
    # 5. Azure PowerShell credentials
    credential = DefaultAzureCredential()
    
    # Create the Azure AI client
    print("Creating Azure AI Foundry client...")
    client = AzureAIFoundryClient(config, credential=credential)
    
    if client.client:
        print("✅ Azure AI client created successfully!")
        print(f"   Endpoint: {config.endpoint}")
        print()
        return client
    else:
        print("❌ Failed to create Azure AI client")
        print("   Verify:")
        print("   1. Your endpoint is correct")
        print("   2. Your credentials are valid (run 'az login' if using CLI)")
        print("   3. You have network connectivity to Azure")
        return None


def test_connection(client):
    """
    SUB-TASK 3: Test the connection to Azure AI services.
    
    Args:
        client: AzureAIFoundryClient instance
        
    Returns:
        bool: True if connection test succeeded, False otherwise
    """
    print("="*60)
    print("SUB-TASK 3: Test Connection")
    print("="*60)
    
    print("Testing connection to Azure AI services...")
    test_result = client.test_connection()
    
    if test_result:
        print("✅ Connection test succeeded!")
        print("   You are now ready to create agents and interact with them.")
        print()
        return True
    else:
        print("❌ Connection test failed")
        print("   Check your endpoint, credentials, or network connectivity")
        print()
        return False


def main():
    """
    Main driver function for Task 1: Creating the Azure AI Client.
    
    This function orchestrates all sub-tasks:
    1. Load configuration from environment
    2. Create the Azure AI client
    3. Test the connection
    
    WORKSHOP INSTRUCTIONS:
    - Initially, all sub-tasks are enabled
    - Instructor will guide you through each sub-task
    - You can comment out sub-tasks to focus on specific steps
    """
    print()
    print("="*60)
    print("TASK 1: Creating the Azure AI Client")
    print("="*60)
    print()
    
    # SUB-TASK 1: Load configuration
    endpoint, config = load_configuration()
    if not config:
        return  # Exit if configuration failed
    
    # SUB-TASK 2: Create the client
    client = create_client(config)
    if not client:
        return  # Exit if client creation failed
    
    # SUB-TASK 3: Test the connection
    test_connection(client)
    
    # Task complete
    print("="*60)
    print("Task 1 Complete!")
    print("="*60)




if __name__ == "__main__":
    main()
