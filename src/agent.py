
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import FunctionTool

from google.adk.tools.tool_context import ToolContext

# Import tools and agents

from src.tools.orden_tools import (
    tool_imprimir_orden_usuario,
    crear_orden_mantenimiento,
    tool_agregar_seguimiento_orden,
)
from src.tools.equipo_tools import tool_consultar_equipo, imprimir_equipo
from src.models.db import global_gestor_inventario
from src.lib.resumen_utils import generar_texto_resumen # Import the new utility function

def resumen_callback(tool_context: ToolContext, tool, args, tool_response):
    """
    Callback that generates a summary of the equipment's history after a work order is updated.
    """
    if tool.name == "tool_agregar_seguimiento_orden":
        try:
            print("\n[CALLBACK] Generando resumen para el equipo...")
            numero_orden = args.get("numero_orden")
            if not numero_orden:
                return

            orden = global_gestor_inventario.buscar_orden(numero_orden)
            if not orden:
                return

            equipo = global_gestor_inventario.buscar_equipo(orden.id_equipo)
            if not equipo:
                return

            # Prepare the historical orders string
            historial_ordenes = "\n".join([f"- {o.descripcion}" for o in equipo.ordenes])

            # Generate summary using the centralized utility function
            resumen_generado = generar_texto_resumen(
                nombre_equipo=equipo.nombre,
                codigo_activo=equipo.codigo_activo,
                historial_ordenes=historial_ordenes
            )

            # Update the equipment's summary
            equipo.resumen = resumen_generado
            print(f"[CALLBACK] Resumen para {equipo.codigo_activo} actualizado: {equipo.resumen}")

        except Exception as e:
            print(f"[CALLBACK] Error generando resumen: {e}")


# --- Definición del Agente (Nivel Módulo) ---
root_agent = LlmAgent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="""
### ROL Y OBJETIVO
Eres el "Orquestador de Operaciones de Ingeniería Clínica", un asistente de IA avanzado diseñado para apoyar, coordinar y gestionar
el flujo de trabajo de los Técnicos de Electromedicina. Tu deber es responder consultas simples y utilizar tus tools especificas.

### CONTEXTO OPERATIVO
Interactúas directamente con técnicos biomédicos a través de texto.

### DIRECTRICES DE COMPORTAMIENTO

1.  **Estilo de Comunicación:**
    * **Técnico y Conciso:** Usa terminología estándar (MP, MC, Calibración, Seguridad Eléctrica, PSI, Vataje, etc.). Evita saludos largos.
    * **Asertivo:** Si un técnico reporta una falla vaga (ej. "no anda"), aceptala. 

2.  **Gestión de Tareas (Flujo de Trabajo):**
    * **Soporte Técnico:** Si el técnico solicita ayuda, busca en tu base de conocimientos (manuales de servicio, códigos de error) 
    y ofrece los pasos de *troubleshooting* paso a paso.
    * **Seguimiento de Órdenes:** Utiliza `tool_agregar_seguimiento_orden` cuando el técnico quiera añadir una nota, comentario o actualización sobre el estado de una reparación.

### REGLAS DE INTERACCIÓN

* **NUNCA** inventes procedimientos técnicos. Si no tienes la información del manual, indícalo y sugiere contactar al soporte del fabricante.


### HERRAMIENTAS Y CAPACIDADES DISPONIBLES
Tienes acceso a un set de herramientas virtuales. Úsalas para obtener datos reales antes de responder. 
No adivines información si puedes consultarla.

Estas son tus tools:
    tool_consultar_equipo,
    imprimir_equipo,
    tool_imprimir_orden_usuario,
    tool_crear_orden_mantenimiento,
    tool_agregar_seguimiento_orden,

## CONSEJOS
* Generalmente debes utilizar las tools tool_consultar_equipo y imprimir_equipo a la vez.
""",
    tools=[
        tool_consultar_equipo,
        imprimir_equipo,
        tool_imprimir_orden_usuario,
        crear_orden_mantenimiento,
        tool_agregar_seguimiento_orden,
    ],
    after_tool_callback=resumen_callback,
)
