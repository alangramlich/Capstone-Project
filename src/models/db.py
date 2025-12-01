from src.models.gestor import GestorInventario
from src.data.loader import cargar_datos_prueba # Import the data loader

# This module holds the global instance of the inventory manager.
# All other modules that need to access the inventory will import this instance.
global_gestor_inventario = GestorInventario()
cargar_datos_prueba(global_gestor_inventario) # Populate the inventory immediately
