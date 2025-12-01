from dataclasses import dataclass, field, asdict
from datetime import date
from typing import List, Optional
from src.models.orden import Orden

@dataclass
class EquipoMedico:
    codigo_activo: str
    identificador_oral: str
    nombre: str
    marca: str
    modelo: str
    numero_serie: str
    ubicacion: str
    dimensiones: str
    resumen: str = "Equipo nuevo"
    
    # Valores por defecto
    estado_operativo: str = "EN_ALMACEN"
    fecha_alta: date = field(default_factory=date.today)
    
    # --- NUEVO: LISTA DE ÓRDENES ---
    # Usamos default_factory=list para que cada equipo tenga su propia lista vacía
    ordenes: List['Orden'] = field(default_factory=list) 

    def agregar_orden(self, orden: 'Orden'):
        """Vincula una orden a este equipo"""
        self.ordenes.append(orden)
        # Opcional: Actualizar estado del equipo si tiene orden pendiente
        if orden.prioridad == "alta":
            self.estado_operativo = "EN_REVISION"

    def obtener_historial_ordenes(self):
        """Devuelve un resumen de las órdenes para el Agente"""
        return [o.to_dict() for o in self.ordenes]

    def to_dict(self):
        """Convierte el equipo a diccionario para pasarlo al LLM (Agente)"""
        data = asdict(self)
        # asdict intenta convertir todo, pero 'ordenes' son objetos complejos.
        # Los sobrescribimos con su versión serializada:
        data['ordenes'] = self.obtener_historial_ordenes()
        # Convertimos fecha a string para que JSON no falle
        data['fecha_alta'] = self.fecha_alta.strftime("%Y-%m-%d")
        return data

    def __str__(self):
        return f"[{self.codigo_activo}] {self.nombre} ({len(self.ordenes)} órdenes)"
