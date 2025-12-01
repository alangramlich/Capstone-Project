from typing import List, Optional
from src.models.equipo import EquipoMedico
from src.models.orden import Orden

class GestorInventario:
    def __init__(self):
        self.base_de_datos: List['EquipoMedico'] = []

    def agregar_equipo(self, equipo):
        self.base_de_datos.append(equipo)
        print(f"✅ Equipo '{equipo.nombre}' agregado.")

    def buscar_equipo(self, termino: str) -> Optional['EquipoMedico']:
        """
        Busca un equipo por código de activo o identificador oral.
        """
        termino = termino.lower().strip()

        for equipo in self.base_de_datos:
            match_codigo = equipo.codigo_activo.lower() == termino
            match_oral = equipo.identificador_oral.lower() == termino

            if match_codigo or match_oral:
                return equipo 
        
        return None

    def listar_todos(self):
        print(f"\n--- INVENTARIO ({len(self.base_de_datos)} equipos) ---")
        for eq in self.base_de_datos:
            print(f"{eq.codigo_activo} | {eq.nombre} | Órdenes: {len(eq.ordenes)}")

    def buscar_orden(self, numero_orden) -> Optional[Orden]:
        """
        Busca una orden por su identificador numérico.
        Acepta int o str (ej: 2 o "2").
        """
        try:
            # Convertimos a int para asegurar la comparación correcta
            id_buscado = int(numero_orden)
        except ValueError:
            print(f"⚠️ Error: '{numero_orden}' no es un número válido.")
            return None

        for equipo in self.base_de_datos:
            for orden in equipo.ordenes:
                # Ahora comparamos int contra int
                if orden.id_orden == id_buscado:
                    return orden
        
        print(f"⚠️ No se encontró la orden #{id_buscado}")
        return None
