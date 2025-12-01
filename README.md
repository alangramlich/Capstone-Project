# Project: Clinical Engineering Operations Orchestrator

This project implements an AI assistant, the "Clinical Engineering Operations Orchestrator," designed to optimize the workflow of biomedical technicians.

## Main Features

- **Work Order Management:** Updates maintenance orders for medical equipment.
- **Inventory Inquiry:** Access to the history of any registered clinical equipment.
- **Automatic Summary Generation:** After adding a follow-up note to an order, the system writes a summary of frequent failures, materials, and the status of the medical equipment.

## How to Get Started

### 1. Prerequisites

- Python 3.9 or higher.
- A Google API key.

### 2. Configuration

1.  **Clone the repository:**

2.  **Install dependencies:**
    Create a virtual environment and install the necessary packages.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configure the API key:**
    Create a file named `.env` in the project root and add your Google API key:
    ```
    GOOGLE_API_KEY="YOUR_API_KEY_HERE"
    ```

### 3. Execution

This application is designed to run with the ADK CLI. To start the web interface, run the following command in your terminal:

```bash
adk web
```

This will spin up a local server with the user interface to interact with the agent.
When the project starts, an inventory of 10 medical devices with registered maintenance orders is generated in memory (loader.py).
Additionally, a call is made to generate summaries for the equipment, which are created from the follow-ups of the maintenance orders. Each time a follow-up line is added, the LLM is also called to update this summary.

# How does this help my work?

The main problem I set out to solve is that in my job, the database used does not allow for easy searching of the comments section of orders, which is the richest section of information, as technicians write down the steps taken, follow-ups, and sometimes guides on how to change parts or configure equipment. The main objective of the project was to implement a RAG agent to answer questions about equipment failures, with the ability to perform semantic searches on the characteristic equipment manual and also by consulting the comments section of orders for that equipment model.

**This objective was not achieved.**

However, the system presented in this Project helped me explore more LLM functionality options. The possibility of creating a summary for each piece of equipment was not in my plans, and while this implementation is not the best, it could be refined to easily generate a general summary of the status of equipment for an entire clinic, or the status of equipment managed by each provider to facilitate preparation for meetings with them.

## Project Structure

```
.
├── .env                  # Environment variables file (API Key)
├── app.py                # ADK application entry point
├── requirements.txt      # Python dependencies
├── src/
│   ├── agent.py          # Main agent definition (root_agent) and its instructions
│   ├── data/
│   │   └── loader.py     # Loads test data into the in-memory database
│   ├── lib/
│   │   └── resumen_utils.py # Utility for generating history summaries
│   ├── models/           # Defines data structures (Equipment, Order, etc.) and the DB manager
│   └── tools/            # Tools the agent can execute (query equipment, create order, etc.)
└── ...
```

# Thank you for teaching this course!