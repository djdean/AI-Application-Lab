# Azure AI Foundry: Create an Agent in the Portal

This guide walks you through creating and testing an Agent in Azure AI Foundry (ai.azure.com) directly in the portal, then shows where to find connection details to use it from code.

## Prerequisites
- Azure subscription with access to Azure AI Foundry (formerly Azure AI Studio).
- An Azure AI Foundry Project you can create resources in.
- At least one model available 


## 1) Open Azure AI Foundry and select your Project
1. Go to https://portal.azure.com and sign in.
2. Pick your Project:
   - If creating a new Project: choose name, region, and resource group.

## 2) Create a new Agent
1. In the Project left navigation, select **Agents**.
2. Click **+ New agent**.

## 3) Agent Setup
1. Select a model deployment to use from the dropdown **Deployment** selector on the right.
2. Give your agent a name by chaning the default provided in the **Agent name** field.
3. Give you agent the following **Instructions**: "You are a helpful assistant. Answer the user's questions to the best of your ability. Try adding some humor to your responses when possible."
## 4) Save and Test
1. The agent should autosave but scroll to the bottom of the Setup panel and click the save icon to ensure the agent is updated. 
2. Scroll to the top of the Setup panel and click "Try in playground"
3. Ask the agent a simple quesiton like "Hello, how are you today?" and look at the response. 
4. Click the "Thread logs" button to view the details of the execution.
5. Click the "View code" button to view the code to use the agent programatically. 
## 5) Change the prompt and repeat
1. Change the **Instruction** in the setup pane on the right to something else such as: "You are a helpful assistant. Answer the user's questions to the best of your ability. Try adding some sarcasm to your responses when possible."
2. Try asking some simple questions as before and view the response.

## Tips and best practices
- **Precise Instructions**: Be explicit about goals, style, and constraints.
