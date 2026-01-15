import logging
from azure_client import AzureAIFoundryClient, AzureAIConfig
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Main function to demonstrate creating an Azure AI client."""
    # Replace with your actual Azure AI Foundry endpoint
    endpoint="https://AIWorkshopTest.services.ai.azure.com/api/projects/test-project",  # Replace with your endpoint
    credential=DefaultAzureCredential()
    config = AzureAIConfig(
        endpoint=endpoint,
        agent_id="your-agent-id"
    )
    
    client = AzureAIFoundryClient(config, credential=credential)
    
    if client.client:
        logger.info("Azure AI client created successfully!")
        logger.info(f"Endpoint: {config.endpoint}")
        test_result = client.test_connection()
        if test_result:
            logger.info("Connection test succeeded!")
        else:
            logger.error("Connection test failed")
    else:
        logger.error("Failed to create Azure AI client")


if __name__ == "__main__":
    main()
