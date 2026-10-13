# 📋 To-Do List API (Flask + PostgreSQL)

API RESTful completa construida con **Python Flask** y persistencia en **PostgreSQL** para la gestión de tareas (To-Do List). Incluye interfaz interactiva web y soporte para pruebas directas desde el navegador o mediante herramientas como cURL / PowerShell / Postman.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **Flask 3.0** (Framework web y API REST)
- **Flask-SQLAlchemy 3.1** (ORM para interactuar con la base de datos)
- **psycopg2-binary** (Driver de conexión a PostgreSQL)
- **Flask-CORS** (Soporte para peticiones cross-origin)
- **python-dotenv** (Gestión de variables de entorno)

---

## 📁 Estructura del Proyecto

```text
TO-DO/
├── app/
│   ├── __init__.py         # Factoría de la aplicación Flask
│   ├── config.py           # Configuración y conexión a PostgreSQL
│   ├── models.py           # Modelo Task y esquemas de BD
│   ├── routes.py           # Endpoints de la API REST
│   └── templates/
│       └── index.html      # Panel web interactivo para pruebas en el navegador
├── venv/                   # Entorno virtual de Python
├── .env                    # Variables de entorno locales
├── .env.example            # Plantilla de variables de entorno
├── .gitignore              # Archivos ignorados por Git
├── requirements.txt        # Dependencias del proyecto
├── init_db.py              # Script para crear la BD y tablas en PostgreSQL
├── run.py                  # Script principal para iniciar el servidor
├── test_api.py             # Pruebas unitarias automatizadas
└── README.md               # Esta documentación
```

---

## 🚀 Paso a Paso: Configuración y Ejecución

### 1. Activar el Entorno Virtual

En PowerShell / Terminal:
```powershell
.\venv\Scripts\Activate.ps1
```
*(Si no estuviera creado, se crea con `python -m venv venv` y se instalan las dependencias con `pip install -r requirements.txt`).*

---

### 2. Configurar la Conexión a PostgreSQL en `.env`

Abre el archivo [`.env`](file:///c:/Users/Usuario/Desktop/TO-DO/.env) y ajusta tus credenciales de PostgreSQL si tu contraseña o usuario son diferentes:

```ini
# Configuración del servidor Flask
FLASK_APP=run.py
FLASK_ENV=development
PORT=5000

# Credenciales de tu PostgreSQL local
DB_USER=postgres
DB_PASSWORD=tu_contraseña_aqui
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todo_db

DATABASE_URL=postgresql://postgres:tu_contraseña_aqui@localhost:5432/todo_db
```

---

### 3. Crear la Base de Datos y las Tablas

Ejecuta el script automático de inicialización:

```powershell
python init_db.py
```

Este script se conectará a PostgreSQL, creará la base de datos `todo_db` si no existe y creará la tabla `tasks`.

---

### 4. Iniciar el Servidor de la API

Inicia el servidor Flask:

```powershell
python run.py
```

Verás un mensaje como:
```text
>>> API To-Do List Iniciada
[*] Interfaz y Documentacion: http://127.0.0.1:5000/
[*] Endpoint Tareas:           http://127.0.0.1:5000/api/tasks
[*] Endpoint Health Check:     http://127.0.0.1:5000/api/health
```

---

## 🌐 Cómo Probar la API en tu Navegador

### Opción A: Interfaz Gráfica Integrada (Recomendada)
Abre tu navegador (Chrome, Edge, Firefox) y entra a:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

En este panel podrás:
1. **Crear** tareas con título y descripción.
2. **Listar** y filtrar (Todas, Pendientes, Terminadas) y buscador en tiempo real.
3. **Terminar** tareas con un clic (botón ✅ Terminar).
4. **Editar** el título y descripción de cualquier tarea existente (botón ✏️).
5. **Eliminar** tareas (botón 🗑️).
6. Ver el estado de salud de la conexión a PostgreSQL en tiempo real.

---

### Opción B: URLs Directas en el Navegador (Peticiones GET)

En cualquier pestaña del navegador puedes abrir directamente:
- **Listar todas las tareas (JSON):**  
  [http://127.0.0.1:5000/api/tasks](http://127.0.0.1:5000/api/tasks)
- **Filtrar solo tareas pendientes:**  
  [http://127.0.0.1:5000/api/tasks?completed=false](http://127.0.0.1:5000/api/tasks?completed=false)
- **Filtrar solo tareas terminadas:**  
  [http://127.0.0.1:5000/api/tasks?completed=true](http://127.0.0.1:5000/api/tasks?completed=true)
- **Buscar tareas con una palabra clave:**  
  [http://127.0.0.1:5000/api/tasks?search=comprar](http://127.0.0.1:5000/api/tasks?search=comprar)
- **Ver detalle de una tarea específica (ejemplo ID 1):**  
  [http://127.0.0.1:5000/api/tasks/1](http://127.0.0.1:5000/api/tasks/1)
- **Verificar estado del servicio y conexión a la BD:**  
  [http://127.0.0.1:5000/api/health](http://127.0.0.1:5000/api/health)

---

## 💻 Comandos de Consola para Pruebas (PowerShell / cURL)

Dado que los navegadores solo ejecutan solicitudes `GET` desde la barra de direcciones, para probar los métodos `POST`, `PUT`, `PATCH` y `DELETE` desde la consola puedes usar:

### Desde PowerShell (Windows):

```powershell
# 1. Crear una tarea (POST)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/tasks" -Method Post -ContentType "application/json" -Body '{"title": "Preparar informe mensual", "description": "Revisar metricas y ventas"}'

# 2. Listar todas las tareas (GET)
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/tasks" -Method Get

# 3. Editar una tarea (PUT) - ID 1
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/tasks/1" -Method Put -ContentType "application/json" -Body '{"title": "Preparar informe anual", "description": "Actualizado"}'

# 4. Terminar una tarea (PATCH) - ID 1
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/tasks/1/complete" -Method Patch

# 5. Eliminar una tarea (DELETE) - ID 1
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/tasks/1" -Method Delete
```

### Desde cURL:

```bash
# 1. Crear una tarea
curl -X POST http://127.0.0.1:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar cafe", "description": "En grano tostado"}'

# 2. Listar tareas
curl -X GET http://127.0.0.1:5000/api/tasks

# 3. Editar tarea con ID 1
curl -X PUT http://127.0.0.1:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar cafe colombiano"}'

# 4. Terminar tarea con ID 1
curl -X PATCH http://127.0.0.1:5000/api/tasks/1/complete

# 5. Eliminar tarea con ID 1
curl -X DELETE http://127.0.0.1:5000/api/tasks/1
```

---

## 📌 Tabla de Endpoints de la API

| Método | Endpoint | Descripción | Parámetros / Body |
|---|---|---|---|
| `GET` | `/` | Panel interactivo web para probar la API | - |
| `GET` | `/api/health` | Estado del servidor y conexión a PostgreSQL | - |
| `GET` | `/api/tasks` | Listar tareas registradas | Query: `?completed=true\|false`, `?search=texto`, `?order=asc\|desc` |
| `GET` | `/api/tasks/<id>` | Detalle de una tarea específica | `id` en la URL |
| `POST` | `/api/tasks` | Crear una nueva tarea | JSON: `{"title": "...", "description": "..."}` |
| `PUT` | `/api/tasks/<id>` | Editar título, descripción o estado | JSON: `{"title": "...", "description": "...", "completed": true\|false}` |
| `PATCH` | `/api/tasks/<id>/complete` | Marcar tarea como terminada | Opcional JSON: `{"completed": false}` para desmarcar |
| `DELETE` | `/api/tasks/<id>` | Eliminar una tarea por ID | `id` en la URL |

---

## 🧪 Ejecución de Tests Automatizados

Para verificar que todos los endpoints y validaciones funcionen sin errores:

```powershell
python test_api.py
```
