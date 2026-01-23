# MCP Inventory Management Agent

This project demonstrates how to connect AI agents to tools using the **Model Context Protocol (MCP)**. The implementation creates an intelligent inventory management agent for a cosmetics retailer that can automatically discover and use tools to analyze inventory levels and provide actionable recommendations.

## 🎯 What You'll Build

- **MCP Client** (`client.py`): An Azure AI agent that connects to MCP servers and automatically uses discovered tools
- **MCP Server** (`server.py`): A local server providing inventory management tools via MCP protocol
- **Interactive Chat**: A conversational interface where the agent analyzes inventory and provides smart recommendations

## 🏗️ Architecture Overview

```
┌─────────────────┐    MCP Protocol    ┌─────────────────┐
│   Azure AI      │ ◄─────────────────► │   MCP Server    │
│   Agent Client  │   (stdio transport) │   (server.py)   │
│   (client.py)   │                     │                 │
└─────────────────┘                     └─────────────────┘
         │                                       │
         │ Calls tools automatically             │ Provides tools:
         │ based on user queries                 │ • get_inventory_levels
         └───────────────────────────────────────│ • get_weekly_sales
```

## 📋 Prerequisites

Before running this project, ensure you have:

1. **Python 3.10+** installed
2. **Azure AI Foundry project** with deployed models
3. **Git** (for cloning the repository)
4. **Azure authentication** set up

## 🚀 Quick Start

### Step 1: Clone and Setup Environment

```bash
# Clone the repository
git clone <repository-url>
cd agentic-ai-lab

# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Configure Azure Authentication

The project uses the existing `.env` configuration. Authenticate using one of these methods:

**Option A: Azure CLI (Recommended)**
```bash
az login
```

**Option B: Environment Variables**
The `.env` file already contains your Azure project configuration.

### Step 3: Verify Your Configuration

The project will automatically use these values from the root `.env` file:
- `AZURE_AI_PROJECT_ENDPOINT`: Your Azure AI project endpoint
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`: Your deployed model (currently: `gpt-4o`)

### Step 4: Run the MCP Demo

The client automatically starts the MCP server, so you only need one command:

```bash
cd 3.BuildAgentsWithMCP
python client.py
```

You should see output like:
```
Project Endpoint: https://your-project.services.ai.azure.com/api/projects/your-project
Model Deployment: gpt-4o
Connected to server with tools: ['get_inventory_levels', 'get_weekly_sales']
Enter a prompt for the inventory agent. Use 'quit' to exit.
USER: 
```

**Note**: The client.py automatically:
1. Starts the MCP server (`server.py`) internally
2. Establishes the MCP protocol connection 
3. Discovers available tools
4. Creates the Azure AI agent with tool access
5. Provides the interactive chat interface

### Step 5: Test the Agent

Try these example prompts:

```
Please analyze our current inventory and provide recommendations

What items need restocking urgently?

Which products should we put on clearance sale?

Show me all inventory levels and sales data

What's our overall inventory health?
```

Type `quit` to exit the application.

## 📁 Project Structure

```
HandOnTasks/
├── 3.BuildAgentsWithMCP/              # 👈 MCP demonstration
│   ├── client.py                # MCP client with Azure AI integration
│   ├── server.py                # MCP server with inventory tools
│   └── README.md               # This file

```

## 🔧 How It Works

### MCP Server (`server.py`)
- **FastMCP Framework**: Lightweight server implementation
- **Inventory Tools**: Provides realistic cosmetics inventory data
- **Sales Tools**: Returns weekly sales figures for analysis
- **stdio Transport**: Communicates with client via standard input/output

### MCP Client (`client.py`)  
- **Automatic Server Launch**: Starts `server.py` as a subprocess using stdio transport
- **Tool Discovery**: Automatically detects available MCP tools from the launched server
- **Dynamic Integration**: Wraps MCP tools as callable Python functions
- **Azure AI Agent**: Creates intelligent agent with access to tools
- **Auto Function Calling**: Agent decides when and how to use tools
- **Conversation Management**: Handles multi-turn conversations with tool usage

### Key Features

1. **Automatic Tool Discovery**: Client discovers server tools without hardcoding
2. **Intelligent Recommendations**: Agent provides business insights based on data
3. **Real-time Analysis**: Tools are called dynamically based on user queries  
4. **Professional Output**: Structured recommendations with reasoning
5. **Error Handling**: Robust error handling and graceful degradation

## 💡 Example Interaction

```
USER: Please analyze our current inventory and provide recommendations

🔧 Agent is calling MCP tools...
📊 Calling tool: get_inventory_levels
📊 Calling tool: get_weekly_sales

AGENT:
Based on the current inventory levels and weekly sales data, here are my recommendations:

**URGENT RESTOCK NEEDED:**
- Moisturizer: Only 6 units left but sold 22 last week - HIGH DEMAND
- Shampoo: Only 8 units left but sold 18 last week - RESTOCK IMMEDIATELY
- Skin Serum: Only 9 units left but sold 19 last week - LOW STOCK ALERT

**CLEARANCE RECOMMENDATIONS:**
- Body Spray: 28 units in stock but only 3 sold - EXCESS INVENTORY
- Cleanser: 30 units in stock but only 4 sold - CONSIDER PROMOTION
- Dry Shampoo: 45 units in stock, selling moderately - MONITOR

**BUSINESS INSIGHTS:**
- Top performers: Moisturizer, Shampoo, and Skin Serum show strong demand
- Slow movers: Body care products need marketing attention
- Inventory turnover: Focus on high-velocity skincare items
```

## 🛠️ Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'mcp'"**
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

**"DefaultAzureCredential failed"**
```bash
# Authenticate with Azure
az login

# Or check if you're signed into VS Code with Azure Account extension
```

**"Server connection failed"**
- The client automatically starts the server, so this error indicates:
  - `server.py` file is missing or corrupted
  - Python environment issues preventing server startup
  - File permissions preventing execution
- Ensure you're in the `agents-with-mcp` directory when running `python client.py`
- Check that virtual environment is activated

**"Agent creation failed"**  
- Verify your `.env` file has correct Azure project details
- Check that your deployed model name matches `AZURE_AI_MODEL_DEPLOYMENT_NAME`
- Ensure you have proper permissions in Azure AI Foundry

### Debug Mode

Add logging to troubleshoot issues:

```python
# Add to top of client.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎓 Learning Objectives

After completing this demo, you'll understand:

1. **MCP Protocol**: How AI agents discover and use external tools
2. **stdio Transport**: Communication between MCP clients and servers  
3. **Azure AI Integration**: Connecting MCP tools to Azure AI agents
4. **Dynamic Function Calling**: How agents decide when to use tools
5. **Business Intelligence**: Converting raw data into actionable insights

## 🔄 Next Steps

**Extend the Demo:**
- Add more inventory tools (purchase orders, supplier data)
- Connect to real inventory databases
- Implement different recommendation algorithms
- Add visualization tools

**Deploy to Production:**  
- Host MCP server in Azure Container Apps
- Use Azure AI Foundry for agent deployment
- Implement authentication and rate limiting
- Add comprehensive error handling and logging

**Explore Other MCP Servers:**
- Try the [Azure MCP Server](https://github.com/Azure/azure-mcp) 
- Build custom MCP servers for your business needs
- Integrate with external APIs and services

## 📚 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Azure AI Foundry](https://ai.azure.com/)
- [Azure AI Agents SDK](https://learn.microsoft.com/en-us/python/api/azure-ai-agents/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)

## 🐛 Support

For issues:
- **Azure AI Services**: [Azure Support](https://azure.microsoft.com/support/)
- **MCP Protocol**: [MCP Community](https://modelcontextprotocol.io/community/)  
- **This Demo**: Create an issue in the repository

---

**🎉 Happy Building!** This demo shows the power of MCP for creating intelligent, tool-aware AI agents that can adapt to different business scenarios.
