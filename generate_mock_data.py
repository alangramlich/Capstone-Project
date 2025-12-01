import random
from datetime import date, timedelta
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Sample data for Equipos
nombres_equipo = ["Respirador", "Monitor de Paciente", "Bomba de Infusión", "Electrocardiógrafo", "Desfibrilador"]
marcas = ["Dräger", "Philips", "Mindray", "GE Healthcare", "Medtronic"]
ubicaciones = ["UCI", "Quirófano 1", "Planta 3 Habitación 301", "Almacén Central", "Emergencias"]
dimensiones = ["120x60x80 cm", "40x30x25 cm", "20x15x35 cm"]

# Sample data for Órdenes
descripciones_orden = [
    "El equipo no enciende",
    "Muestra un error en la pantalla",
    "Necesita calibración",
    "Fuga de aire en el circuito",
    "Batería no carga",
    "Realizar mantenimiento preventivo"
]
prioridades = ["alta", "media", "baja"]

# Sample data for Seguimientos
comentarios_seguimiento = [
    "El técnico ha sido asignado y se espera que revise el equipo en las próximas 24 horas.",
    "Se ha realizado una inspección inicial. Parece ser un problema con la fuente de alimentación.",
    "Esperando la llegada de una pieza de repuesto (batería modelo XYZ).",
    "La pieza ha llegado. Se procederá con la reparación.",
    "El equipo ha sido reparado y está en fase de pruebas.",
    "Pruebas finalizadas con éxito. El equipo está operativo.",
    "El equipo ha sido devuelto a su ubicación original y está listo para su uso."
]

def generar_equipos(cantidad):
    equipos = []
    for i in range(cantidad):
        nombre = random.choice(nombres_equipo)
        marca = random.choice(marcas)
        modelo = f"{marca}-{random.randint(100, 999)}"
        equipo = {
            "codigo_activo": f"EQ{2023001 + i}",
            "identificador_oral": f"Equipo {i+1}",
            "nombre": nombre,
            "marca": marca,
            "modelo": modelo,
            "numero_serie": f"SN-{random.randint(10000, 99999)}",
            "ubicacion": random.choice(ubicaciones),
            "dimensiones": random.choice(dimensiones),
            "resumen": f"Este es un resumen del equipo de tipo {nombre}",
            "estado_operativo": "EN_ALMACEN",
            "fecha_alta": (date.today() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "ordenes": []
        }
        equipos.append(equipo)
    return equipos

def generar_seguimientos(fecha_creacion_orden):
    seguimientos = []
    num_seguimientos = random.randint(1, 5)
    fecha_seguimiento = fecha_creacion_orden
    for _ in range(num_seguimientos):
        # Aseguramos que el seguimiento sea posterior a la creación
        fecha_seguimiento += timedelta(days=random.randint(1, 3))
        comentario = random.choice(comentarios_seguimiento)
        seguimientos.append(f"{fecha_seguimiento.strftime('%d.%m.%Y')}. {comentario}")
    return seguimientos

def generar_ordenes(cantidad, equipos):
    for i in range(cantidad):
        equipo_asignado = random.choice(equipos)
        fecha_creacion = date.today() - timedelta(days=random.randint(1, 30))
        orden = {
            "id_orden": 1001 + i,
            "id_equipo": equipo_asignado["codigo_activo"],
            "descripcion": random.choice(descripciones_orden),
            "prioridad": random.choice(prioridades),
            "estado": random.choice(["PENDIENTE", "CERRADA"]),
            "fecha_creacion": fecha_creacion.strftime("%Y-%m-%d"),
            "seguimiento": generar_seguimientos(fecha_creacion)
        }
        equipo_asignado["ordenes"].append(orden)
    return equipos # Devuelve los equipos actualizados con sus órdenes

def main():
    num_equipos = 20
    num_ordenes = 50

    equipos_generados = generar_equipos(num_equipos)
    equipos_actualizados = generar_ordenes(num_ordenes, equipos_generados)

    # El EscritorResumenes actualizará el campo 'resumen' directamente en los objetos de equipo.

    with open("mock_data.txt", "w", encoding="utf-8") as f:
        f.write("--- EQUIPOS MÉDICOS ---\n\n")
        for equipo in equipos_actualizados:
            f.write(f"Código Activo: {equipo['codigo_activo']}\n")
            f.write(f"  Nombre: {equipo['nombre']}\n")
            f.write(f"  Marca/Modelo: {equipo['marca']} {equipo['modelo']}\n")
            f.write(f"  Ubicación: {equipo['ubicacion']}\n")
            f.write(f"  Fecha de Alta: {equipo['fecha_alta']}\n")
            f.write(f"  Resumen: {equipo['resumen']}\n\n")


        f.write("\n--- ÓRDENES DE TRABAJO ---\n\n")
        for equipo in equipos_actualizados:
            for orden in equipo["ordenes"]:
                f.write(f"ID Orden: {orden['id_orden']}\n")
                f.write(f"  ID Equipo: {orden['id_equipo']}\n")
                f.write(f"  Descripción: {orden['descripcion']}\n")
                f.write(f"  Prioridad: {orden['prioridad']}\n")
                f.write(f"  Estado: {orden['estado']}\n")
                f.write(f"  Fecha Creación: {orden['fecha_creacion']}\n")
                if orden["seguimiento"]:
                    f.write("  Seguimiento:\n")
                    for seg in orden["seguimiento"]:
                        f.write(f"    - {seg}\n")
                f.write("\n")

    print(f"Datos generados en 'mock_data.txt': {num_equipos} equipos y {num_ordenes} órdenes.")

if __name__ == "__main__":
    main()
