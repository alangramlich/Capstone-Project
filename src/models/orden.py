import uuid
from datetime import datetime

class Orden:
    _contador_id = 0 

    def __init__(self, id_equipo, descripcion, prioridad="media", **kwargs):
        self.id_orden = Orden._contador_id 
        Orden._contador_id += 1 
        
        self.id_equipo = id_equipo
        self.descripcion = descripcion 
        self.prioridad = prioridad
        self.estado = "PENDIENTE"
        self.datos_extra = kwargs
        self.fecha_creacion = datetime.now()
        
        # --- CAMPOS PARA RAG ---
        self.fecha_cierre = None
        self.materiales = []   # <--- Renombrado (antes piezas_cambiadas)
        self.seguimiento = []  # <--- NUEVO CAMPO

    def agregar_seguimiento(self, comentario: str):
        """Añade una nueva entrada de seguimiento con fecha automática."""
        fecha_actual = datetime.now().strftime("%d.%m.%Y")
        self.seguimiento.append(f"{fecha_actual}. {comentario}")
        print(f"Seguimiento añadido a la orden {self.id_orden}: '{comentario}'")



    def cerrar_orden(self, materiales: list = None, notas_cierre: str = None):
        """
        Cierra la orden. 'materiales' puede incluir repuestos y consumibles.
        Ej: ["Batería 12V", "Alcohol Isopropílico", "Paño"]
        Ahora valida que exista al menos un seguimiento.
        """
        if notas_cierre:
            self.agregar_seguimiento(f"Nota de cierre: {notas_cierre}")

        if not self.seguimiento:
            error_msg = f"Error: No se puede cerrar la orden #{self.id_orden} porque no tiene comentarios de seguimiento."
            print(f"❌ {error_msg}")
            return error_msg
            
        self.estado = "CERRADA"
        self.fecha_cierre = datetime.now()

        if materiales:
            self.materiales = materiales
            
        success_msg = f"✅ Orden #{self.id_orden} cerrada. Informe guardado."
        print(success_msg)
        return success_msg

    def obtener_documento_rag(self, modelo_equipo: str = ""):
        """
        Genera el texto 'rico' para Vector Search.
        """
        if self.estado != "CERRADA":
            return None
            
        # Estructura optimizada para búsqueda
        texto_rag = (
            f"EQUIPO: {modelo_equipo} | "
            f"SÍNTOMA: {self.descripcion} | "
            f"MATERIALES: {', '.join(self.materiales) if self.materiales else 'Ninguno'}"
        )
        return texto_rag
        
    def to_dict(self):
        """Convierte la orden a diccionario para pasarlo al LLM (Agente)"""
        return {
            "id": self.id_orden,
            "equipo": self.id_equipo,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad,
            "estado": self.estado,
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
            "fecha_cierre": self.fecha_cierre.strftime("%Y-%m-%d %H:%M") if self.fecha_cierre else None,

            "materiales": self.materiales,
            "seguimiento": self.seguimiento, # <--- NUEVO
            **self.datos_extra
        }

