# Azure AI Foundry Agents - Hands-On Workshop

## Overview

This hands-on workshop teaches you how to programmatically create and interact with AI agents using the Azure AI Foundry SDK. You'll learn the core concepts and practical skills needed to integrate intelligent agents into your applications.

## Learning Objectives

By the end of this workshop, you will be able to:

1. **Initialize and configure** an Azure AI Foundry client with proper authentication
2. **Create agents programmatically** using custom models and instructions
3. **Manage agent lifecycle**, including creation, retrieval, and deletion
4. **Establish conversations** with agents and maintain conversation context
5. **Send messages** to agents and process their responses
6. **Retrieve conversation history** and analyze interaction patterns
7. **Handle agent-generated files** such as charts and data visualizations
8. **Implement error handling** for robust agent interactions

## Prerequisites

### Technical Requirements
- Python 3.8 or higher
- Azure subscription with access to Azure AI Foundry
- Visual Studio Code or preferred Python IDE

### Required Knowledge
- Basic Python programming
- Understanding of async/await patterns in Python
- Familiarity with environment variables and configuration management

### Azure Setup
Before starting the workshop, ensure you have:
- An Azure AI Foundry project endpoint URL
- An AI agent deployed in your Azure AI Foundry project
- Appropriate Azure credentials configured for authentication

## Workshop Structure

This workshop consists of three progressive tasks that build upon each other:

### Task 1: Creating the Azure AI Client
**Duration:** 15 minutes

Learn the fundamentals of initializing the Azure AI Foundry client, understanding configuration requirements, and establishing a connection to your Azure AI services.

**Key Concepts:**
- AzureAIConfig dataclass
- DefaultAzureCredential authentication
- Client initialization and validation

### Task 2: Create an Agent Programmatically
**Duration:** 20 minutes

Discover how to create, retrieve, and manage AI agents entirely through code, enabling dynamic agent deployment in your applications.

**Key Concepts:**
- Agent creation with custom models
- Configuring agent instructions and behavior
- Agent lifecycle management
- Retrieving agent details
- Cleaning up resources

### Task 3: Complete Agent Communication Workflow
**Duration:** 30 minutes

Master the complete workflow for interacting with agents, from starting conversations to processing complex responses and handling generated files.

**Key Concepts:**
- Conversation thread management
- Message exchange patterns
- Response processing
- Conversation history retrieval
- File content handling and downloads

## Getting Started

### 1. Install Dependencies

Navigate to the workshop directory and install required packages:

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Set up your Azure credentials as environment variables:

```bash
# Windows PowerShell
$env:AZURE_AI_PROJECT_ENDPOINT = "your-endpoint-url"
$env:AZURE_AI_AGENT_ID = "your-agent-id"

# Linux/macOS
export AZURE_AI_PROJECT_ENDPOINT="your-endpoint-url"
export AZURE_AI_AGENT_ID="your-agent-id"
```

### 3. Import the Shared Module

All tasks utilize the `azure_client.py` module which contains the `AzureAIFoundryClient` class and supporting data structures. This eliminates code duplication and provides a consistent interface across all exercises.

### 4. Work Through Tasks Sequentially

Start with Task 1 and progress through each task in order. Each task builds upon concepts from previous tasks.

## Workshop Materials

- `azure_client.py` - Shared client module with all Azure AI functionality
- `task_1_create_client.py` - Client initialization exercise
- `task_1.md` - Task 1 objectives and instructions
- `task_2_create_agent.py` - Agent creation and management exercise
- `task_2.md` - Task 2 objectives and instructions
- `task_3_agent_communication.py` - Complete communication workflow exercise
- `task_3.md` - Task 3 objectives and instructions
- `requirements.txt` - Python package dependencies

## Key Concepts Reference

### AzureAIConfig
Configuration dataclass containing:
- `endpoint` - Your Azure AI Foundry project endpoint
- `agent_id` - The ID of your deployed agent

### ChatMessage
Represents a message in a conversation:
- `role` - Message sender (user/assistant)
- `content` - Message text
- `timestamp` - When the message was sent

### AgentResponse
Structured response from the agent:
- `message` - Text response from the agent
- `charts` - List of chart file IDs (if generated)
- `error` - Error message (if any)

## Best Practices

1. **Error Handling**: Always implement try-except blocks when making API calls
2. **Resource Cleanup**: Delete agents you create programmatically to manage costs
3. **Async Operations**: Use async/await properly for non-blocking operations
4. **Logging**: Utilize logging for debugging and monitoring agent interactions
5. **Environment Variables**: Never hardcode credentials; use environment variables

## Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify your Azure credentials are properly configured
- Ensure you have appropriate permissions in your Azure subscription

**Connection Issues:**
- Confirm your endpoint URL is correct
- Check network connectivity to Azure services

**Agent Not Found:**
- Verify the agent ID matches an existing agent in your project
- Ensure the agent is in a running state

## Additional Resources

- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure AI Projects SDK Reference](https://learn.microsoft.com/python/api/overview/azure/ai-projects-readme)
- [Azure Identity Documentation](https://learn.microsoft.com/python/api/overview/azure/identity-readme)

## Support

For questions or issues during the workshop:
1. Review the task-specific markdown files for detailed guidance
2. Check the troubleshooting section above
3. Consult the Azure AI Foundry documentation
4. Reach out to workshop facilitators

---

**Ready to begin?** Start with [Task 1: Creating the Azure AI Client](task_1.md)
