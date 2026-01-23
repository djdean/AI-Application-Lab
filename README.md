# 🚀 Microsoft Foundry & Agents Workshop

[![Microsoft Foundry](https://img.shields.io/badge/Microsoft-Foundry-blue?style=for-the-badge&logo=microsoft)](https://ai.azure.com)
[![Python](https://img.shields.io/badge/Python-3.10+-green?style=for-the-badge&logo=python)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Lab-orange?style=for-the-badge&logo=jupyter)](https://jupyter.org)

**End-to-End Microsoft Foundry And Agents Development Laboratory**

*Master Microsoft Foundry and Agents through hands-on experimentation and real-world applications*


## 🎯 Mission Statement

This comprehensive laboratory transforms you from an AI enthusiast into a Microsoft Foundry expert. Through progressive, hands-on modules, you'll master:

1. **Prompt Engineering (Portal)**
   - Chat with AI pattern in prompt messages (call center, image description extraction)
   - Hands-on exercises based on GitHub instructions

2. **AI Search**
   - Creating an index via Azure Portal
   - Chat over data in Playground connected to portal-created index
   - SDK approach: Creating an index using notebooks and Python code
   - Uploading data and creating indexes programmatically
   - Chat over data in Playground connected to SDK-created index

3. **Foundry SDK for LLM Communication**
   - Direct interaction with Large Language Models using SDK

4. **Agent Framework with DevUI**
   - Interactive chatting with agents using SDK and DevUI features

5. **Creating Agents in Portal**
   - Portal-based agent creation and configuration

6. **Foundry Agents with Capabilities**
   - Code Interpreter integration
   - Knowledge - Agent access to AI Search indexes created in previous labs

7. **Microsoft Foundry SDK - Advanced Agent Capabilities**
   - Leveraging agents with multiple capabilities

8. **Workflow in Agent Framework**
   - Sequential streaming workflow examples

9. **LangGraph with Workflow**
   - Advanced workflow orchestration using LangGraph

10. **Technical Deep Dive (Demo & Hands-on)**
    - FastAPI implementation
    - Streamlit integration (library installation and setup)
    - Model Context Protocol (MCP) - Client and Server architecture


---

## 📁 Repository Structure

```
Pfizer-AI-labs/
├── .env.template              # Environment variables template (copy to .env)
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── requirements.txt           # Python dependencies
│
├── Day1/                      # Day 1: Foundry Basics & Prompt Engineering
│   ├── HandsOnTasks/
│   │   ├── 1.PromptEngineering.md
│   │   ├── 2.CreatingAISearchInPortal.md
│   │   ├── 3.PlaygroundToAccessIndex.md
│   │   └── Task 1.md
│   ├── Slides/
│   └── UseCases/
│
├── Day2/                      # Day 2: Agents with Capabilities
│   ├── HandsOnTasks/
│   │   ├── 1.CodeInterpreter-DJ.md
│   │   ├── 2.AgentToAccessIndex.md
│   │   └── Task 1.md
│   ├── Slides/
│   └── UseCases/
│
├── Day3/                      # Day 3: SDK & Advanced Agent Development
│   ├── HandsOnTasks/
│   │   ├── 1.AISearch/                    # AI Search with SDK
│   │   │   ├── search_queries.ipynb
│   │   │   ├── setup_search_index.ipynb
│   │   │   └── upload_to_blob.ipynb
│   │   ├── 2.ConnectToAIProgramatically/  # SDK Connection Methods
│   │   │   ├── ConnectToProjectClient.py
│   │   │   ├── ConnectViaAPIKey.py
│   │   │   └── ConnectViaBearerToken.py
│   │   ├── 3.InteractWithAIAgents/        # Agent Interaction Tasks
│   │   │   ├── azure_client.py
│   │   │   ├── task_1_create_client.py
│   │   │   ├── task_2_create_agent.py
│   │   │   └── task_3_agent_communication.py
│   │   ├── 4.AzureOpenAIChatClient_devui.py  # Agent Framework DevUI
│   │   ├── 5.Sequential_streaming.py         # Workflow Streaming
│   │   └── 6.CreateLanggraphWorkflow/        # LangGraph Workflows
│   │       ├── task_1_workflow.py
│   │       └── task_2_workflow.py
│   ├── Slides/
│   └── UseCases/
│
├── Day4/                      # Day 4: Technical Deep Dive
│   ├── HandsOnTasks/
│   │   ├── 1.BuildFastAPIServer/          # FastAPI Implementation
│   │   │   ├── task_1-5_server.py         # Progressive server builds
│   │   │   └── test_task_*.py             # Test files
│   │   ├── 2.BuildStreamlitServer/        # Streamlit Integration
│   │   │   ├── task_1-4_app.py            # Progressive app builds
│   │   │   └── test_task_*.py             # Test files
│   │   └── 3.BuildAgentsWithMCP/          # Model Context Protocol
│   │       ├── client.py                  # MCP Client with Azure AI
│   │       ├── server.py                  # MCP Server with tools
│   │       └── README.md                  # MCP detailed instructions
│   ├── Slides/
│   └── UseCases/
│
└── images/                    # Documentation images
```

---
## 🚀 Getting Started

### Step 1: Repository Setup

```powershell
# Clone the laboratory repository
git clone <repository-url>
cd Pfizer-AI-labs

# Verify Python version (if not using DevContainer)
python --version  # Python 3.10+ required
```

### Step 2: Choose Your Development Environment

You have two options for setting up your development environment:

#### Local Python Environment (Standard venv)

If you prefer a local setup or don't have Docker:

```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install all dependencies with locked versions for reproducibility
pip install -r requirements.txt
```

> **💡 Note:** This project uses pip for dependency management to ensure consistent installations across all environments.
>
> To update dependencies, edit `requirements.txt` directly and run `pip install -r requirements.txt`.


### Step 3: Microsoft Foundry Setup

1. **Create Microsoft Foundry Resource and Project**
   
   To create a Microsoft Foundry resource in the Azure portal follow these instructions:

   - Select this Microsoft Foundry resource link: https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry

   - On the Create page, provide the following information:

   <img src="images/ai-foundry-deployment.png" width="75%"/>

   | Project details | Description |
   |----------------|-------------|
   | **Subscription** | Select one of your available Azure subscriptions. |
   | **Resource group** | The Azure resource group that will contain your Azure AI Foundry resource. You can create a new group or add it to a preexisting group. |
   | **Region** | The location of your Azure AI service instance. Different locations may introduce latency, but have no impact on the runtime availability of your resource. |
   | **Name** | A descriptive name for your Microsoft Foundry resource. For example, MyAIServicesResource. |
   | **Default Project Name** | Keep the default project as it is. |

   - Keep other settings for your resource as default, read and accept the conditions (as applicable), and then select **Review + create**.

2. **Assign Azure AI User Role**
   
   **Important:** Developers and lab attendees must be assigned the **Azure AI User** role to interact with the Microsoft Foundry project:
   
   - **Recommended:** Assign at the **Project level**
   - **Alternative:** If encountering permission issues, assign at the **Foundry Resource level**
   
   This role provides the necessary permissions to deploy models, create agents, and execute AI operations.
   
   For detailed guidance, follow the [Role-based access control for Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry?view=foundry-classic) documentation.
   
3. **Deploy Required Models & Services**
   
   | Model Type | Recommended Models | Purpose |
   |------------|-------------------|---------|
   | **Chat/Completion** | `gpt-4o`, `gpt-4o-mini` | Primary reasoning & conversation |
   | **Text Embeddings** | `text-embedding-3-large` | Vector search & RAG |

   - On the left Nav Menu of the foundry portal go to Models+endpoints
   - Click Deploy a model button-->Deploy base model
      - Search for the models in the table above , select a model, click confirm and Deploy and connect
       <img src="images/deploy-models.png" width="75%"/>

4. **Configure an Azure Search Service**
   - Create an Azure AI Search resource in Azure
   - Connect this resource to your Microsoft Foundry project
      - Navigate to your Microsoft Foundry project → Management Center → Connected Resources → Add Connection → Select Azure AI Search
      <img src="images/foundry-connection.png" width="75%"/>
  
5. **Configure Environment Variables**
   - Copy `.env.template` to `.env` in the root directory and update values accordingly
   - This repository expects the `.env` file to be in the root directory, if you want to store it elsewhere or name it something else, update the `load_dotenv()` calls in notebooks
   - Many of the Environment Variables needed can be found in the Overview tab of your Microsoft Foundry project or the connected resources in the Management Center tab
   - For example, AZURE_OPENAI variables-
<img src="images/env-example.png" width="75%"/>  

---
---

## 🛠️ Troubleshooting & Support

### ⚡ Common Issues & Solutions

**Kernel Issues in VS Code:**
```powershell
# Refresh kernel registration
python -m ipykernel install --user --name=ai-foundry-lab --display-name="AI Foundry Lab"
# Reload VS Code: Ctrl+Shift+P → "Developer: Reload Window"
```

**Environment Activation Problems:**
```powershell
# Set PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Verify virtual environment
python -c "import sys; print(sys.executable)"
```

**Azure Authentication Issues:**
```powershell
# Recommended: Use Azure CLI authentication
az login --tenant YOUR_TENANT_ID
az account show

# Alternative: Clear cached credentials and re-login
az account clear
az login --tenant YOUR_TENANT_ID
az account show
```

> **Note:** If you see deprecation warnings about the Azure Account extension in VS Code, use `az login` in the terminal instead. The Azure Account extension for VS Code has been deprecated in favor of Azure CLI authentication.

### 📚 Additional Resources

- 📖 [Microsoft Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/)
- 🎥 [Video Tutorials](https://learn.microsoft.com/en-us/shows/ai-show/)
- 💡 [Best Practices Guide](https://learn.microsoft.com/en-us/azure/ai-services/responsible-use-of-ai-overview)

