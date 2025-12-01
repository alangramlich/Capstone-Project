import logging
import os
from dotenv import load_dotenv

from google.adk.apps.app import App
from google.adk.sessions import InMemorySessionService
from google.adk.memory import InMemoryMemoryService

from src.agent import root_agent
from src.models.db import global_gestor_inventario
from src.data.loader import cargar_datos_prueba

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- App Constants ---
APP_NAME = "clinical_engineering_orchestrator"
USER_ID = "default_user"

# --- App Initialization ---
logger.info("--- Initializing ADK App ---")

# Load environment variables
load_dotenv()

# API Key Check
if "GOOGLE_API_KEY" not in os.environ or not os.environ["GOOGLE_API_KEY"]:
    logger.error(
        "🔑 Authentication Error: 'GOOGLE_API_KEY' not found or is empty. "
        "Please create a .env file and add your key."
    )
    raise ValueError("API Key not configured.")
else:
    logger.info("✅ GOOGLE_API_KEY found.")

# Load data
cargar_datos_prueba(global_gestor_inventario)

# Create services
memory_service = InMemoryMemoryService()
session_service = InMemorySessionService()

# Create and assign the ADK App to the global 'app' variable
app = App(
    name=APP_NAME,
    root_agent=root_agent
)

logger.info("--- ADK App initialized successfully ---")

if __name__ == "__main__":
    logger.info("ADK App setup complete. To run the Web UI, execute 'adk web' in your terminal.")
    logger.info("Ensure you have 'adk' installed and properly configured.")