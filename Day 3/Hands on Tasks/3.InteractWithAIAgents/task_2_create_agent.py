"""
TASK 2: Create an Agent Programmatically

Objective:
Learn how to create and configure an AI agent using the Azure AI Projects SDK.
This task demonstrates the complete lifecycle of agent management:
- Creating a new agent with specific configuration
- Retrieving agent details to verify creation
- Cleaning up by deleting the agent when done

Learning Goals:
- Understand how to create agents programmatically (not just via UI)
- Learn about agent configuration options (model, instructions, tools)
- Practice retrieving agent information
- Understand the importance of resource cleanup

What You'll Learn:
- How to use create_agent() with parameters like model, name, and instructions
- How agent instructions shape AI behavior
- How to retrieve and inspect agent properties
- Best practices for resource management (cleanup)

Key Concepts:
- Agent: An AI entity configured with specific instructions and tools
- Instructions: The system prompt that guides the agent's behavior
- Model: The LLM backbone (e.g., "gpt-4o")
- Deployment: Where the agent runs in Azure

Why This Matters:
Creating agents programmatically allows you to:
1. Automate agent creation in production workflows
2. Create agents with dynamic configurations
3. Test different agent behaviors systematically
4. Integrate agent creation into larger applications
"""

import os
import asyncio
from dotenv import load_dotenv
from azure_client import AzureAIFoundryClient, AzureAIConfig
from azure.identity import DefaultAzureCredential

# Load environment variables from .env file
load_dotenv()


def load_configuration():
    """
    Load and validate configuration from environment variables.
    
    Returns:
        tuple: (endpoint, model, config, credential) or (None, None, None, None) if validation fails
    """
    endpoint = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT")
    model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")
    
    if not endpoint:
        print("❌ AZURE_AI_FOUNDRY_ENDPOINT not found in environment variables")
        print("   Please copy .env.example to .env and fill in your endpoint")
        return None, None, None, None
    
    print(f"Configuration loaded from .env:")
    print(f"  Endpoint: {endpoint}")
    print(f"  Model: {model}")
    print()
    
    config = AzureAIConfig(endpoint=endpoint)
    credential = DefaultAzureCredential()
    
    return endpoint, model, config, credential


async def subtask_1_create_agent(client, model):
    """
    SUB-TASK 1: Create an AI agent programmatically.
    
    Args:
        client: AzureAIFoundryClient instance
        model: Model deployment name to use
        
    Returns:
        str: Agent ID if successful, None otherwise
    """
    print("=" * 60)
    print("SUB-TASK 1: Create Agent")
    print("=" * 60)
    print("Creating a new agent with the following configuration:")
    print("  - Model: gpt-4o (the GPT-4 Omni model)")
    print("  - Name: workshop-agent (descriptive identifier)")
    print("  - Instructions: System prompt that guides behavior")
    print()
    
    # WORKSHOP TASK: Create a new agent with specific configuration
    # Try modifying the instructions to test different behaviors!
    agent_id = await client.create_agent(
        model=model,
        name="workshop-agent",
        instructions="You are a helpful AI assistant that provides clear and concise answers to questions."
    )
    
    if not agent_id:
        print("❌ Failed to create agent")
        print("   Possible causes:")
        print("   1. Model is not deployed in your account")
        print("   2. Authentication failed")
        print("   3. API quota exceeded")
        print("   4. Network connectivity issue")
        return None
    
    print(f"✅ Agent created successfully!")
    print(f"   Agent ID: {agent_id}")
    print(f"   Save this ID - you'll need it to use this agent!")
    print()
    
    return agent_id


async def subtask_2_retrieve_agent(client, agent_id):
    """
    SUB-TASK 2: Retrieve and display agent details.
    
    Args:
        client: AzureAIFoundryClient instance
        agent_id: ID of the agent to retrieve
        
    Returns:
        object: Agent object if successful, None otherwise
    """
    print("=" * 60)
    print("SUB-TASK 2: Retrieve Agent Details")
    print("=" * 60)
    print("Fetching the agent configuration we just created...")
    print()
    
    agent = await client.get_agent(agent_id)
    
    if not agent:
        print("❌ Failed to retrieve agent")
        print("   The agent might have been deleted or is inaccessible")
        return None
    
    print("✅ Agent retrieved successfully!")
    print(f"   Name: {agent.name if hasattr(agent, 'name') else 'N/A'}")
    print(f"   Model: {agent.model if hasattr(agent, 'model') else 'N/A'}")
    if hasattr(agent, 'instructions'):
        instructions = agent.instructions[:50] + "..." if len(str(agent.instructions)) > 50 else agent.instructions
        print(f"   Instructions: {instructions}")
    print(f"   Status: Active and ready to use")
    print()
    
    return agent


async def subtask_3_delete_agent(client, agent_id):
    """
    SUB-TASK 3: Delete the agent (cleanup).
    
    Args:
        client: AzureAIFoundryClient instance
        agent_id: ID of the agent to delete
        
    Returns:
        bool: True if deletion succeeded, False otherwise
    """
    print("=" * 60)
    print("SUB-TASK 3: Delete Agent (Cleanup)")
    print("=" * 60)
    print("Deleting the agent to free up resources...")
    print()
    
    success = await client.delete_agent(agent_id)
    
    if success:
        print("✅ Agent cleanup completed successfully!")
        print(f"   Agent {agent_id} has been deleted")
        print()
        print("💡 In real applications, you would typically:")
        print("   1. Create an agent once")
        print("   2. Reuse that agent ID across many interactions")
        print("   3. Delete it only when the application is done")
    else:
        print("❌ Failed to delete agent")
        print("   The agent might still exist - you may need to delete it manually")
        print("   or it may have already been deleted")
    
    print()
    return success


async def main():
    """
    Main driver function for Task 2: Create an Agent Programmatically.
    
    This function orchestrates all sub-tasks:
    1. Create Agent - Build a new agent with configuration
    2. Retrieve Agent Details - Fetch and inspect the created agent
    3. Delete Agent - Clean up the agent to free resources
    
    WORKSHOP INSTRUCTIONS:
    - Work through each sub-task one at a time
    - Instructor will guide you through each function
    - Comment out sub-tasks to focus on specific steps:
      # agent_id = await subtask_1_create_agent(client, model)
    """
    print()
    print("=" * 60)
    print("TASK 2: Create an Agent Programmatically")
    print("=" * 60)
    print()
    
    # Load configuration
    endpoint, model, config, credential = load_configuration()
    if not config:
        return
    
    client = AzureAIFoundryClient(config, credential=credential)
    
    # SUB-TASK 1: Create Agent
    agent_id = await subtask_1_create_agent(client, model)
    if not agent_id:
        return
    
    # SUB-TASK 2: Retrieve Agent Details
    agent = await subtask_2_retrieve_agent(client, agent_id)
    if not agent:
        return
    
    # SUB-TASK 3: Delete Agent (Cleanup)
    await subtask_3_delete_agent(client, agent_id)
    
    # Task complete
    print("=" * 60)
    print("Task 2 Complete!")
    print("=" * 60)
    print()
    print("NEXT STEPS:")
    print("1. Review your agent configuration to understand agent creation")
    print("2. Try modifying the instructions to see how it affects behavior")
    print("3. Move to Task 3 to learn how to interact with agents")
    print()


if __name__ == "__main__":
    asyncio.run(main())
