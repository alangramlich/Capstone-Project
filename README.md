# Proyecto: Orquestador de Operaciones de Ingeniería Clínica

Este proyecto implementa un asistente de IA avanzado, el "Orquestador de Operaciones de Ingeniería Clínica", diseñado para optimizar el flujo de trabajo de los técnicos de electromedicina. Utilizando el modelo `gemini-2.5-flash` de Google, el agente gestiona el mantenimiento de equipos clínicos, la creación de órdenes de trabajo y el seguimiento de reparaciones a través de una interfaz conversacional.

## Características Principales

- **Gestión de Órdenes de Trabajo:** Creación y actualización de órdenes de mantenimiento para equipos médicos.
- **Consulta de Inventario:** Acceso rápido a la información y el historial de cualquier equipo clínico registrado.
- **Generación de Resúmenes Automáticos:** Después de añadir una nota de seguimiento a una orden, el sistema utiliza un LLM para generar y actualizar un resumen del historial de mantenimiento del equipo.
- **Interacción Inteligente:** El agente está instruido para comprender la terminología técnica y asistir a los técnicos en sus tareas diarias.
- **Framework ADK:** Construido sobre el App Development Kit (ADK) de Google, lo que permite una integración nativa con los servicios de IA de Google.

## Cómo Empezar

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### 1. Prerrequisitos

- Python 3.9 o superior.
- Una clave de API de Google.

### 2. Configuración

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO>
    ```

2.  **Instala las dependencias:**
    Crea un entorno virtual e instala los paquetes necesarios.
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Configura la clave de API:**
    Crea un archivo llamado `.env` en la raíz del proyecto y añade tu clave de API de Google:
    ```
    GOOGLE_API_KEY="TU_CLAVE_DE_API_AQUI"
    ```

### 3. Ejecución

Esta aplicación está diseñada para ejecutarse con la CLI de ADK. Para iniciar la interfaz web, ejecuta el siguiente comando en tu terminal:

```bash
adk web
```

Esto levantará un servidor local con la interfaz de usuario para interactuar con el agente.

## Estructura del Proyecto

```
.
├── .env                  # Archivo para variables de entorno (API Key)
├── app.py                # Punto de entrada de la aplicación ADK
├── requirements.txt      # Dependencias de Python
├── src/
│   ├── agent.py          # Definición del agente principal (root_agent) y sus instrucciones
│   ├── data/
│   │   └── loader.py     # Carga de datos de prueba en la base de datos en memoria
│   ├── lib/
│   │   └── resumen_utils.py # Utilidad para generar resúmenes de historial
│   ├── models/           # Define las estructuras de datos (Equipo, Orden, etc.) y el gestor de BBDD
│   └── tools/            # Herramientas que el agente puede ejecutar (consultar equipo, crear orden, etc.)
└── ...
```
