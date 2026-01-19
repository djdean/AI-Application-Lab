import asyncio
import logging
from azure_client import AzureAIFoundryClient, AzureAIConfig
from azure.identity import DefaultAzureCredential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main function to demonstrate complete agent communication workflow."""
    # Replace with your actual Azure AI Foundry endpoint and agent ID
    config = AzureAIConfig(
        endpoint="https://AIWorkshopTest.services.ai.azure.com/api/projects/test-project"
    )
    credential = DefaultAzureCredential()
    client = AzureAIFoundryClient(config, credential=credential)
    
    # ============ SUB-TASK 1: START CONVERSATION ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 1: Start Conversation")
    logger.info("=" * 60)
    
    success = await client.start_conversation()
    if not success:
        logger.error("Failed to start conversation")
        return
    
    logger.info("Conversation started successfully!")
    logger.info(f"Thread ID: {client.thread_id}")
    logger.info("")
    
    # ============ SUB-TASK 2: SEND MESSAGE ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 2: Send Message to Agent")
    logger.info("=" * 60)
    user_message = "What is the capital of France?"
    logger.info(f"Sending message: {user_message}")
    logger.info("")
    
    response = await client.send_message(user_message)
    
    if not response or response.error:
        logger.error(f"Failed to send message: {response.error if response else 'No response'}")
        return
    
    # ============ SUB-TASK 3: PROCESS RESPONSE ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 3: Process Agent Response")
    logger.info("=" * 60)
    
    if response.message:
        logger.info(f"Agent response: {response.message}")
    
    if response.charts:
        logger.info(f"Found {len(response.charts)} file(s) in response")
    else:
        logger.info("No files in response")
    logger.info("")
    
    # ============ SUB-TASK 4: GET CONVERSATION HISTORY ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 4: Retrieve Conversation History")
    logger.info("=" * 60)
    
    history = await client.get_conversation_history()
    
    if history:
        logger.info(f"Conversation history ({len(history)} message(s)):")
        logger.info("")
        for i, msg in enumerate(history, 1):
            role_str = msg.role.value if hasattr(msg.role, 'value') else str(msg.role)
            logger.info(f"  Message {i}: [{role_str}]")
            logger.info(f"    Content: {msg.content}")
            if msg.timestamp:
                logger.info(f"    Timestamp: {msg.timestamp}")
            logger.info("")
    else:
        logger.warning("No conversation history found")
    
    # ============ SUB-TASK 5: HANDLE FILE CONTENT (if files exist) ============
    logger.info("=" * 60)
    logger.info("SUB-TASK 5: Handle File Content")
    logger.info("=" * 60)
    
    if response.charts:
        logger.info(f"Processing {len(response.charts)} file(s)...")
        logger.info("")
        
        for chart in response.charts:
            logger.info(f"File: {chart['filename']}")
            logger.info(f"  File ID: {chart['file_id']}")
            logger.info(f"  Type: {chart['type']}")
            
            # Download file content
            file_content = await client.get_file_content(chart['file_id'])
            
            if file_content:
                file_size = len(file_content)
                logger.info(f"  Status: Downloaded ({file_size} bytes)")
                
                # Save to file
                output_path = f"output_{chart['filename']}"
                with open(output_path, "wb") as f:
                    f.write(file_content)
                logger.info(f"  Saved to: {output_path}")
            else:
                logger.warning(f"  Status: Failed to download")
            logger.info("")
    else:
        logger.info("No files to process")
    
    logger.info("=" * 60)
    logger.info("Task Complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
