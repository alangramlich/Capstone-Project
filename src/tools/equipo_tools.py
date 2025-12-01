import json
from src.models.db import global_gestor_inventario

def tool_consultar_equipo(identificador: str) -> str:
    """
    Busca un equipo médico por su identificador 
    (código de activo o nombre oral) y devuelve todos sus detalles técnicos 
    y su historial de órdenes de mantenimiento. El Usuario no lo ve.
    
    Args:
        identificador (str): El código del activo (ej: "EQ-001") o identificador oral (ej: "banana pararrayos copete").
        
    Returns:
        str: Un JSON con la información del equipo o un mensaje de error si no existe.
    """
    equipo = global_gestor_inventario.buscar_equipo(identificador)
    
    if not equipo:
        return f"Error: No se encontró ningún equipo en la base de datos con el identificador '{identificador}'."
    
    info_equipo = equipo.to_dict()
    return json.dumps(info_equipo, indent=2, ensure_ascii=False)

def imprimir_equipo(identificador: str) -> str:
    """
    Busca un equipo médico y DEVUELVE un string con su ficha técnica 
    detallada y formateada para mostrar en la pantalla del usuario.
    
    Ahora incluye el listado específico de Órdenes de Trabajo (Número y Descripción).
    
    Args:
        identificador (str): El código del activo (ej: "EQ-001") o identificador oral.
        
    Returns:
        str: String multi-línea con la ficha técnica o mensaje de error.
    """
    
    equipo = global_gestor_inventario.buscar_equipo(identificador)
    
    if not equipo:
        return f"Error: No se encontró ningún equipo con el identificador '{identificador}'."
    
    data = equipo.to_dict()
    
    reporte = []
    reporte.append("━"*50)
    reporte.append(f"🏥  FICHA TÉCNICA DEL EQUIPO")
    reporte.append("━"*50)
    
    reporte.append(f"🏷️  Nombre:      {data.get('nombre', 'N/A').upper()}")
    reporte.append(f"🆔  ID Activo:   {data.get('codigo_activo', 'N/A')}")
    reporte.append(f"🗣️  ID Oral:     {data.get('identificador_oral', 'N/A')}")
    reporte.append("-" * 50)
    
    reporte.append(f"⚙️  DATOS TÉCNICOS")
    reporte.append(f"    • Marca:     {data.get('marca', 'N/A')}")
    reporte.append(f"    • Modelo:    {data.get('modelo', 'N/A')}")
    reporte.append(f"    • Serie:     {data.get('numero_serie', 'N/A')}")
    reporte.append(f"    • Ubicación: {data.get('ubicacion', 'N/A')}")
    reporte.append("-" * 50)

    # --- NUEVO: RESUMEN DEL EQUIPO ---
    resumen_equipo = data.get('resumen', 'Sin resumen disponible.')
    reporte.append(f"📝  RESUMEN DEL EQUIPO:\n    {resumen_equipo}")
    reporte.append("-" * 50)
    
    ordenes = data.get('ordenes', []) 
    
    reporte.append(f"📂  ÓRDENES ASOCIADAS ({len(ordenes)} registros)")
    
    if not ordenes:
        reporte.append("    No hay órdenes de trabajo registradas para este equipo.")
    else:
        for orden_data in ordenes:
            estado_orden = orden_data.get('estado', 'N/D')
            icono = "🟢" if estado_orden == "CERRADA" else "🟠"
            reporte.append(f"    {icono} OT #{orden_data.get('id', 'N/A')}: {orden_data.get('descripcion', 'Sin descripción')}")
            
    reporte.append("━"*50)

    return "\n".join(reporte)