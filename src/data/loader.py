from src.models.equipo import EquipoMedico
from src.models.orden import Orden
from src.models.gestor import GestorInventario
from src.lib.resumen_utils import generar_texto_resumen # Import the new utility function

def cargar_datos_prueba(gestor_inv: GestorInventario):
    """Carga 10 equipos y órdenes de ejemplo, incluyendo una con informe detallado."""
    
    lista_equipos = [
        EquipoMedico(
            codigo_activo="EQ-001", identificador_oral="caballo francia cangrejo",
            nombre="Ecógrafo", marca="General Electric", modelo="Vivid S70",
            numero_serie="GE-998822", ubicacion="Cardiología - Sala 1", dimensiones="150x60x80 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-002", identificador_oral="mate auto casa",
            nombre="Rayos X Portátil", marca="Philips", modelo="MobileDiagnost wDR",
            numero_serie="PH-RX-002", ubicacion="Emergencias - Box 3", dimensiones="130x60x120 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-003", identificador_oral="pelota cono helado",
            nombre="Bomba de Infusión", marca="Alaris", modelo="GH Plus",
            numero_serie="AL-554433", ubicacion="UTI - Cama 4", dimensiones="15x20x10 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-004", identificador_oral="churros banana fuego",
            nombre="Monitor Multiparamétrico", marca="Spacelabs", modelo="Qube",
            numero_serie="MN-112233", ubicacion="Guardia - Box 2", dimensiones="30x25x15 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-005", identificador_oral="municion fuego caramelo",
            nombre="Desfibrilador", marca="mindray", modelo="D3",
            numero_serie="ZO-778899", ubicacion="Shock Room", dimensiones="40x30x25 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-006", identificador_oral="chocolate crimen avion",
            nombre="Ventilador Mecánico", marca="Hamilton Medical", modelo="C1",
            numero_serie="HM-334455", ubicacion="UTI - Cama 2", dimensiones="50x50x120 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-007", identificador_oral="pistola lapiz violin",
            nombre="Torre de Endoscopia", marca="Olympus", modelo="EVIS EXERA III",
            numero_serie="OL-667788", ubicacion="Quirófano 2", dimensiones="60x70x150 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-008", identificador_oral="termometro auto rojo",
            nombre="Arco en C", marca="Siemens", modelo="Cios Alpha",
            numero_serie="SI-ARC-001", ubicacion="Quirófano 1", dimensiones="200x80x180 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-009", identificador_oral="cuna arbol azul",
            nombre="Cuna de Calor Radiante", marca="Dräger", modelo="Isolette 8000",
            numero_serie="DR-998877", ubicacion="Neonatología", dimensiones="110x60x190 cm"
        ),
        EquipoMedico(
            codigo_activo="EQ-010", identificador_oral="bisturi perro gato",
            nombre="Electrobisturí", marca="Valleylab", modelo="ForceTriad",
            numero_serie="VL-FT-003", ubicacion="Quirófano 3", dimensiones="45x40x20 cm"
        ),
    ]

    for equipo in lista_equipos:
        gestor_inv.agregar_equipo(equipo)

    # Órdenes de ejemplo
    orden1 = Orden(id_equipo="EQ-001", descripcion="No enciende pantalla", prioridad="alta")
    orden2 = Orden(id_equipo="EQ-002", descripcion="Mantenimiento preventivo semestral", prioridad="media")
    orden3 = Orden(id_equipo="EQ-003", descripcion="Alarma de oclusión", prioridad="alta")
    orden4 = Orden(id_equipo="EQ-004", descripcion="Calibración de PNI", prioridad="baja")
    
    # Orden 5 con informe detallado para pruebas RAG/Búsqueda
    orden5 = Orden(id_equipo="EQ-004", descripcion="Pantalla con rayas horizontales, a veces no responde al tacto.", prioridad="alta", tecnico_asignado="Laura Martinez")
    orden5.agregar_seguimiento("28.11.2025. Se realizó diagnóstico inicial, se sospecha fallo en digitalizador.") # Añadido para pasar validación
    orden5.cerrar_orden(
        materiales=["Panel LCD Mindray uMEC 10", "Guantes antiestáticos"]
    )

    # NUEVA ORDEN: Calibración de Bomba de Infusión (EQ-003)
    # Detalle técnico: Fallo de oclusión y calibración en menú de servicio
    orden6 = Orden(
        id_equipo="EQ-003", 
        descripcion="Suena alarma de oclusión recurrentemente", 
        prioridad="alta", 
        tecnico_asignado="Ing. Bio. Carlos Ruiz"
    )
    
    # 1. Agregamos el diagnóstico detallado
    orden6.agregar_seguimiento(
        "29.11.2025. Se revisa el equipo. El nivel de alarma seteado es L3. "
        "Se prueba segun manual setear la bomba en 200 ml/h y testear con un medidor de fuerza a que valor se alarma. "
        "Resultado: Se alarma a 1.2 kgf (Fuera de rango)."
    )
    
    # 2. Cerramos la orden con la solución técnica
    orden6.cerrar_orden(
        notas_cierre="Se realiza calibracion accediendo al menu de ST segun manual. "
                     "Luego de la calibracion se vuelve a testear. Funcionamiento OK, valores de alarma normales. "
                     "Se regresa al servicio.",
        materiales=[] # No requirió repuestos, solo mano de obra/calibración
    )

    # ... (código anterior de asignación de órdenes) ...
    

    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden1)
    gestor_inv.buscar_equipo("EQ-002").agregar_orden(orden2)
    gestor_inv.buscar_equipo("EQ-003").agregar_orden(orden3)
    gestor_inv.buscar_equipo("EQ-004").agregar_orden(orden4)
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden5)
    gestor_inv.buscar_equipo("EQ-003").agregar_orden(orden6)

    # Órdenes para EQ-001
    # Fallas de usuario
    orden_fu_1 = Orden(id_equipo="EQ-001", descripcion="Configurar boton 1", prioridad="media")
    orden_fu_1.agregar_seguimiento("Ingresa el equipo por problemas de impresion. Se revisa la impresora, funciona correctamente. Se configura el boton 1 para que tenga la funcion de imprimir. El Usuario estaba acostumbrado a otra configuracion.") # Comentario para la orden de falla de usuario 1
    orden_fu_1.cerrar_orden(notas_cierre="Se configura el boton 1 para que tenga la funcion de imprimir.", materiales=[])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_fu_1)

    orden_fu_2 = Orden(id_equipo="EQ-001", descripcion="Borrado automatico de estudios", prioridad="media")
    orden_fu_2.agregar_seguimiento("Ingresa el equipo por falla en la memoria. Se revisan estudios guardados, no hay ninguno. Se revisa configuracion y se encuentra que borra automaticamente los estudios cada 30 dias. Se decide no cambiar la configuracion.") # Comentario para la orden de falla de usuario 2
    orden_fu_2.cerrar_orden(notas_cierre="Se decide no cambiar la configuracion de borrado automatico.", materiales=[])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_fu_2)

    orden_fu_3 = Orden(id_equipo="EQ-001", descripcion="Transductor roto", prioridad="media")
    orden_fu_3.agregar_seguimiento("Ingresa el equipo por mala imagen. Se revisan todos los transductores y se encuentra que el transductor tiene una zona con cristales dañados. Se retira el equipo de servicio y se solicita transductor nuevo. Se reemplaza el transductor y el equipo queda funcional.") # Comentario para la orden de falla de usuario 3
    orden_fu_3.cerrar_orden(notas_cierre="Se reemplaza el transductor y el equipo queda funcional.", materiales=["Transductor nuevo"])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_fu_3)

    # Errores en el puerto del transductor
    orden_ept_1 = Orden(id_equipo="EQ-001", descripcion="Errores en el puerto del transductor", prioridad="media")
    orden_ept_1.agregar_seguimiento("Ingresa el equipo por transductor roto. Se revisan los transductores y funcionan perfectamente. Sim embargo, el equipo no reconoce el puerto N3. Se solicita repuesto y se explica al Usuario que el puerto N3 no esta funcional. Ingresa el repuesto, se cambia, y el equipo vuelve a la normalidad.") # Comentario para la orden de error de puerto 1
    orden_ept_1.cerrar_orden(notas_cierre="Se cambia el repuesto del puerto N3 y el equipo vuelve a la normalidad.", materiales=["Repuesto puerto N3"])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_ept_1)

    orden_ept_2 = Orden(id_equipo="EQ-001", descripcion="Sobrecalentamiento", prioridad="media")
    orden_ept_2.agregar_seguimiento("Ingresa el equipo por error de pantalla azul. Se revisa el equipo y se encuentra que la tarjeta grafica no responde. Se revisa el filtro de aire y esta tapado por polvo. Se solicita cambio de placa y se limpia el filtro. El equipo queda funcional.") # Comentario para la orden de error de puerto 2
    orden_ept_2.cerrar_orden(notas_cierre="Se cambia la placa grafica y se limpia el filtro. El equipo queda funcional.", materiales=["Placa grafica"])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_ept_2)

    orden_ept_3 = Orden(id_equipo="EQ-001", descripcion="errores en el puerto del transductor", prioridad="media")
    orden_ept_3.agregar_seguimiento("Ingresa el equipo por transductor roto. Se revisan los transductores y funcionan perfectamente. Sim embargo, el equipo no reconoce el puerto N3. Se solicita repuesto y se explica al Usuario que el puerto N3 no esta funcional. Ingresa el repuesto, se cambia, y el equipo vuelve a la normalidad.") # Comentario para la orden de error de puerto 3
    orden_ept_3.cerrar_orden(notas_cierre="Se cambia el repuesto del puerto N3 y el equipo vuelve a la normalidad.", materiales=["Repuesto puerto N3"])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_ept_3)

    orden_ept_4 = Orden(id_equipo="EQ-001", descripcion="errores en el puerto del transductor", prioridad="media")
    orden_ept_4.agregar_seguimiento("Ingresa el equipo por transductor roto. Se revisan los transductores y funcionan perfectamente. Sim embargo, el equipo no reconoce el puerto N3. Se solicita repuesto y se explica al Usuario que el puerto N3 no esta funcional. Ingresa el repuesto, se cambia, y el equipo vuelve a la normalidad.") # Comentario para la orden de error de puerto 4
    orden_ept_4.cerrar_orden(notas_cierre="Se cambia el repuesto del puerto N3 y el equipo vuelve a la normalidad.", materiales=["Repuesto puerto N3"])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_ept_4)

    orden_ept_5 = Orden(id_equipo="EQ-001", descripcion="Rueda trabada", prioridad="media")
    orden_ept_5.agregar_seguimiento("Ingresa el equipo por rueda trabada. Se desarma y limpia la rueda. El equipo vuelve funcional al servicio.") # Comentario para la orden de error de puerto 5
    orden_ept_5.cerrar_orden(notas_cierre="Se desarma y limpia la rueda. El equipo vuelve funcional al servicio.", materiales=[])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_ept_5)

    # Fallo del trackball
    orden_ft_1 = Orden(id_equipo="EQ-001", descripcion="fallo del trackball", prioridad="media")
    orden_ft_1.agregar_seguimiento("Ingresa el equipo por trackball trabado. Se desarma el teclado y limpia el trackball. Vuelve a la normalidad.") # Comentario para la orden de fallo de trackball 1
    orden_ft_1.cerrar_orden(notas_cierre="Se desarma el teclado y limpia el trackball. Vuelve a la normalidad.", materiales=[])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_ft_1)

    orden_ft_2 = Orden(id_equipo="EQ-001", descripcion="fallo del trackball", prioridad="media")
    orden_ft_2.agregar_seguimiento("Ingresa el equipo por trackball trabado. Se desarma el teclado y limpia el trackball. Vuelve a la normalidad.") # Comentario para la orden de fallo de trackball 2
    orden_ft_2.cerrar_orden(notas_cierre="Se desarma el teclado y limpia el trackball. Vuelve a la normalidad.", materiales=[])
    gestor_inv.buscar_equipo("EQ-001").agregar_orden(orden_ft_2)

    print("\n✅ Datos de prueba cargados en el gestor.")

    # --- Generación de Resúmenes ---
    print("\n--- Iniciando Generación de Resúmenes de Mantenimiento ---")
    for equipo in gestor_inv.base_de_datos:
        if not equipo.ordenes:
            # print(f"ℹ️ No hay órdenes para el equipo {equipo.codigo_activo}, no se generará resumen.")
            continue

        historial_ordenes_list = []
        for o in equipo.ordenes:
            historial_ordenes_list.append(f"- Título de la orden: {o.descripcion}")
            if o.seguimiento:
                seguimientos_str = "\n  ".join([f"  - {s}" for s in o.seguimiento])
                historial_ordenes_list.append(f"  Seguimientos:\n  {seguimientos_str}")
        historial_ordenes = "\n".join(historial_ordenes_list)

        # Generate summary using the centralized utility function
        print(f"🔄 Generando resumen para el equipo: {equipo.codigo_activo}...")
        resumen_generado = generar_texto_resumen(
            nombre_equipo=equipo.nombre,
            codigo_activo=equipo.codigo_activo,
            historial_ordenes=historial_ordenes
        )

        # Update the equipment's summary
        equipo.resumen = resumen_generado
        print(f"✅ Resumen para '{equipo.codigo_activo}' guardado.")
    print("\n--- Finalizada la Generación de Resúmenes ---")