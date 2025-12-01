import json
from google.adk.tools.tool_context import ToolContext
from src.models.db import global_gestor_inventario
from src.models.orden import Orden
from typing import Optional

def tool_imprimir_orden_usuario(numero_orden: str) -> str:
    """
    Busca una Orden de Trabajo y DEVUELVE un string formateado para mostrar 
    en la pantalla del usuario, incluyendo el INFORME TÉCNICO y MATERIALES.
    
    Usa esta herramienta cuando el usuario pida explícitamente:
    "muéstrame la orden", "imprimir orden", "ver estado de la OT", "ver reporte", etc.
    
    Args:
        numero_orden (str): El número de la orden a mostrar.
        
    Returns:
        str: Un string multi-línea con el reporte formateado o un mensaje de error.
    """
    orden = global_gestor_inventario.buscar_orden(numero_orden)
    
    if not orden:
        return f"Error: No se encontró la orden {numero_orden}."
    
    data = orden.to_dict()
    
    estado = data.get('estado', 'Desconocido').upper()
    icono_estado = "🟢" if estado == "CERRADA" else "🟠" if estado == "PENDIENTE" else "🔴"
    
    # Construir el reporte como una lista de strings
    reporte = []
    reporte.append("═"*60)
    reporte.append(f"📄  ORDEN DE TRABAJO: #{data.get('id', numero_orden)}")
    reporte.append("═"*60)
    
    reporte.append(f"📅  Creada:      {data.get('fecha_creacion', 'S/F')}")
    if 'fecha_cierre' in data and data['fecha_cierre']:
        reporte.append(f"🏁  Cerrada:     {data['fecha_cierre']}")
        
    reporte.append(f"🏥  Equipo ID:   {data.get('equipo', 'N/A')}")
    reporte.append("-" * 60)
    
    reporte.append(f"📊  ESTADO:      {icono_estado} {estado}")
    reporte.append(f"📝  DESCRIPCIÓN DEL PROBLEMA:")
    reporte.append(f"    {data.get('descripcion', 'Sin descripción.')}")
    
    seguimientos = data.get('seguimiento', [])
    if seguimientos:
        reporte.append("-" * 60)
        reporte.append(f"👣  SEGUIMIENTO ({len(seguimientos)} entradas):")
        for seg in seguimientos:
            reporte.append(f"    - {seg}")
    
    informe = data.get('informe_tecnico')
    if informe:
        reporte.append("-" * 60)
        reporte.append("📋  INFORME TÉCNICO ASOCIADO:")
        reporte.append(informe)

    materiales = data.get('materiales', [])
    if materiales:
        reporte.append("-" * 60)
        reporte.append("🔩  MATERIALES UTILIZADOS:")
        for mat in materiales:
            reporte.append(f"    - {mat}")

    reporte.append("═"*60)
    
    # Unir la lista en un solo string con saltos de línea y devolver
    return "\n".join(reporte)

def tool_agregar_seguimiento_orden(numero_orden: str, comentario: str) -> str:
    """
    Añade un comentario de seguimiento a una orden de trabajo existente.
    
    Args:
        numero_orden (str): El número o ID de la orden a la que se agregará el comentario.
        comentario (str): El texto del comentario de seguimiento.
        
    Returns:
        str: Confirmación de que el seguimiento fue añadido o un mensaje de error.
    """
    orden = global_gestor_inventario.buscar_orden(numero_orden)
    
    if not orden:
        return f"Error: No se encontró la orden {numero_orden} para agregarle un seguimiento."
    
    orden.agregar_seguimiento(comentario)
    
    return f"Éxito: Se agregó el seguimiento a la orden #{numero_orden}."



def crear_orden_mantenimiento(termino_equipo: str, descripcion: str, prioridad: str = "media", tecnico: Optional[str] = None) -> str:
    """
    Crea y registra una nueva orden de trabajo o mantenimiento para un equipo médico.
    
    Args:
        termino_equipo (str): El identificador del equipo (ej: 'EQ-001' o 'carro chicle').
        descripcion (str): Explicación clara del problema o tarea.
        prioridad (str, opcional): 'alta', 'media' o 'baja'. Default: 'media'.
        tecnico (str, opcional): Nombre del técnico asignado (si aplica).

    Returns:
        str: El ID de la nueva orden generada (ej: '5') o mensaje de error.
    """
    equipo = global_gestor_inventario.buscar_equipo(termino_equipo)
    
    if not equipo:
        print(f"\n❌ ERROR: No se encontró el equipo '{termino_equipo}'.")
        return f"Error: No se encontró ningún equipo que coincida con '{termino_equipo}'."
    
    nueva_orden = Orden(
        id_equipo=equipo.codigo_activo, 
        descripcion=descripcion, 
        prioridad=prioridad, 
        tecnico=tecnico
    )
    
    equipo.agregar_orden(nueva_orden)
    
    print("\n" + "━"*50)
    print(f"✅  NUEVA ORDEN REGISTRADA")
    print("━"*50)
    print(f"🔢  ID Orden:     {nueva_orden.id_orden}")
    print(f"🏥  Equipo:       {equipo.nombre} ({equipo.codigo_activo})")
    print(f"📝  Descripción:  {descripcion}")
    print(f"🚨  Prioridad:    {prioridad.upper()}")
    if tecnico:
        print(f"👷  Técnico:      {tecnico}")
    print("━"*50 + "\n")
    
    return str(nueva_orden.id_orden)