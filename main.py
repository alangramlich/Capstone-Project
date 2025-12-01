import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from src.agent import root_agent
from src.models.db import global_gestor_inventario
import os
from dotenv import load_dotenv

async def main():
    """
    Example of how to run the agent and trigger the summary generation callback.
    """
    print("--- Running agent to trigger summary generation ---")

    # Load environment variables
    load_dotenv()
    if "GOOGLE_API_KEY" not in os.environ or not os.environ["GOOGLE_API_KEY"]:
        print("🔑 Authentication Error: 'GOOGLE_API_KEY' not found or is empty.")
        return

    # --- Setup Runner and Session ---
    session_service = InMemorySessionService()
    app_name = "clinical_engineering_orchestrator"
    user_id = "test_user"
    session_id = "test_session"

    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    runner = Runner(
        agent=root_agent,
        app_name=app_name,
        session_service=session_service,
    )

    # --- Get an existing order and equipment ---
    orden = global_gestor_inventario.buscar_orden("0")
    if not orden:
        print("Error: Order with ID 0 not found.")
        return

    equipo = global_gestor_inventario.buscar_equipo(orden.id_equipo)
    if not equipo:
        print(f"Error: Equipment with ID {orden.id_equipo} not found.")
        return

    print(f"Initial summary for equipment {equipo.codigo_activo}: {equipo.resumen}")

    # --- Run the agent to trigger the tool call ---
    prompt = f"Agregar el siguiente seguimiento a la orden {orden.id_orden}: 'Se realizó una prueba de funcionamiento y el equipo opera correctamente.'"
    content = types.Content(role="user", parts=[types.Part(text=prompt)])
    
    print("\nRunning agent with prompt:", prompt)
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.is_final_response():
            print("Agent's final response:", event.content.parts[0].text)

    # --- Check the updated summary ---
    print(f"\nFinal summary for equipment {equipo.codigo_activo}: {equipo.resumen}")
    
    # --- Print the equipment with the updated summary ---
    from src.tools.equipo_tools import imprimir_equipo
    print("\n--- Equipo Details after Summary Update ---")
    print(imprimir_equipo(equipo.codigo_activo))
    print("------------------------------------------")


if __name__ == "__main__":
    asyncio.run(main())
