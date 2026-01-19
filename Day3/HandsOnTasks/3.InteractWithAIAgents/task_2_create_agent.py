import asyncio
import logging
from azure_client import AzureAIFoundryClient, AzureAIConfig
from azure.identity import DefaultAzureCredential
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main function to demonstrate creating an agent programmatically."""
    # Replace with your actual Azure AI Foundry endpoint
    config = AzureAIConfig(
        endpoint="https://AIWorkshopTest.services.ai.azure.com/api/projects/test-project"
    )
    credential = DefaultAzureCredential()
    client = AzureAIFoundryClient(config, credential=credential)
    
    # ============ SUB-TASK 1: CREATE AGENT ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 1: Create Agent")
    logger.info("=" * 60)
    
    agent_id = await client.create_agent(
        model="gpt-4o",
        name="workshop-agent",
        instructions="You are a helpful AI assistant that provides clear and concise answers to questions."
    )
    
    if not agent_id:
        logger.error("Failed to create agent")
        return
    
    logger.info("")
    
    # ============ SUB-TASK 2: RETRIEVE AGENT DETAILS ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 2: Retrieve Agent Details")
    logger.info("=" * 60)
    
    agent = await client.get_agent(agent_id)
    
    if not agent:
        logger.error("Failed to retrieve agent")
        return
    
    logger.info("")
    
    # ============ SUB-TASK 3: DELETE AGENT ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 3: Delete Agent (Cleanup)")
    logger.info("=" * 60)
    
    success = await client.delete_agent(agent_id)
    
    if success:
        logger.info("Agent cleanup completed successfully!")
    else:
        logger.error("Failed to delete agent")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Task Complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
