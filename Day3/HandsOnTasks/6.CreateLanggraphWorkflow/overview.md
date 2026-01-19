# Create a LangGraph Workflow - Overview

## Introduction
This lab walks you through building a minimal LangGraph that delegates reasoning to an Azure AI Foundry Agent. You will run everything locally while the model and agent live in Azure.

## What You'll Learn
- Wiring LangGraph state and nodes
- Calling an Azure AI Foundry Agent from Python
- Handling chat state and threads
- Polling runs and reading agent messages

## Prerequisites
- Python 3.10+
- An Azure AI Foundry Agent with a deployed model and permissions to run it
- Endpoint and agent ID for the resource
- Authentication via either an API key or Azure Active Directory (DefaultAzureCredential)

## Structure
- Task 1: Build and run a single-node LangGraph that proxies to your Azure AI Foundry Agent
- Task 2 (optional): Add a summarizer node to demonstrate branching and multiple runs

## How to Start
1. Install dependencies with `pip install -r requirements.txt`.
2. Copy `.env.example` to `.env` and add your Azure values.
3. Open [task_1.md](Create%20Langgraph%20Workflow/task_1.md) and follow the steps.
