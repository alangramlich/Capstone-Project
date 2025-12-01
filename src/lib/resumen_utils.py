import os
import google.generativeai as genai

def generar_texto_resumen(nombre_equipo: str, codigo_activo: str, historial_ordenes: str) -> str:
    """
    Genera un resumen conciso del estado de un equipo médico utilizando un LLM.

    Args:
        nombre_equipo: Nombre del equipo.
        codigo_activo: Código activo del equipo.
        historial_ordenes: String con el historial de órdenes de mantenimiento.

    Returns:
        Un string con el resumen generado.
    """
    prompt = f"""
    Analiza el siguiente historial de órdenes de trabajo para el equipo '{nombre_equipo}' ({codigo_activo}) y genera un resumen conciso de su estado.

    Historial de órdenes:
    {historial_ordenes}

    El resumen debe incluir:
    - Estado general del equipo.
    - Fallas más frecuentes (basado en la descripción de las órdenes).
    - Repuestos que se utilizan comúnmente (si se mencionan en los informes).

    Resumen:
    """

    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash') # Reverted for debugging
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"ERROR al generar resumen con LLM para {codigo_activo}: {e}")
        return f"ERROR: No se pudo generar resumen automático. {e}"
