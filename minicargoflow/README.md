# Mini CargoFlow V1

Mini CargoFlow es una API REST educativa para la gestión y seguimiento de envíos en un contexto logístico. El proyecto está pensado para aprender Python, FastAPI, SQLAlchemy, Pydantic y pruebas con Pytest, priorizando código simple, legible y fácil de estudiar.

## 1. Descripción del proyecto

La aplicación permite:

- Registrar envíos.
- Consultar envíos por ID, listado paginado o número de guía.
- Actualizar información de un envío.
- Cambiar el estado de un envío con validación de transiciones.
- Cancelar un envío.
- Consultar el historial de trazabilidad por ID o por número de guía.

### Stack tecnológico

- Python 3.12+ (probado con Python 3.13 de Laragon)
- FastAPI
- MySQL 8
- SQLAlchemy 2.x
- Pydantic
- PyMySQL
- Uvicorn
- python-dotenv
- Pytest

## 2. Requisitos previos

- Windows con PowerShell.
- Python 3.12 o superior.
- MySQL 8 (en este entorno se usó MySQL 8.4.3 incluido en Laragon).
- Acceso a un usuario MySQL con permisos para crear bases de datos.

## 3. Instalación de Python

Verifica si Python está instalado:

```powershell
python --version
```

Si usas Laragon, también puedes usar la ruta directa:

```powershell
C:\laragon\bin\python\python-3.13\python.exe --version
```

Si no tienes Python 3.12+, descárgalo desde https://www.python.org/downloads/ e instala marcando la opción para agregar Python al PATH.

## 4. Creación del entorno virtual

Desde la carpeta del proyecto:

```powershell
cd C:\laragon\www\elitelogistica\minicargoflow
C:\laragon\bin\python\python-3.13\python.exe -m venv .venv
```

## 5. Activación del entorno virtual en Windows

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts, puedes permitirlo para el usuario actual:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego vuelve a ejecutar el comando de activación.

## 6. Instalación de dependencias

Con el entorno virtual activo:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 7. Configuración de MySQL

Inicia MySQL desde Laragon. Luego crea las bases de datos de desarrollo y pruebas:

```powershell
& "C:\laragon\bin\mysql\mysql-8.4.3-winx64\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS minicargoflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE DATABASE IF NOT EXISTS minicargoflow_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

> Nota: en ambientes Laragon comunes, el usuario es `root` y la contraseña suele estar vacía. Ajusta el comando si tu entorno usa credenciales diferentes.

## 8. Configuración del archivo `.env`

Copia el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

Ejemplo de contenido:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=minicargoflow
DB_USER=root
DB_PASSWORD=
DB_NAME_TEST=minicargoflow_test

DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/minicargoflow
DATABASE_URL_TEST=mysql+pymysql://root:@127.0.0.1:3306/minicargoflow_test
```

No incluyas credenciales reales en el repositorio. El archivo `.env` está ignorado por Git.

## 9. Ejecución del proyecto

Con el entorno virtual activo y desde `minicargoflow/`:

```powershell
python run.py
```

O directamente con Uvicorn:

```powershell
uvicorn app.main:app --reload
```

La API quedará disponible en:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json

### Decisión sobre tablas

En esta V1, las tablas se crean automáticamente al iniciar la aplicación mediante `Base.metadata.create_all()` en `app/main.py`. Es una decisión didáctica para simplificar el arranque. En una evolución futura se recomienda usar **Alembic** para migraciones versionadas.

## 10. Ejecución de pruebas

Las pruebas usan la base de datos `minicargoflow_test`, separada de la base de desarrollo. Antes de cada prueba se eliminan y recrean las tablas para asegurar aislamiento.

Ejecuta:

```powershell
pytest -v
```

## 11. Explicación de la estructura de carpetas

```text
minicargoflow/
├── app/
│   ├── __init__.py              # Marca app como paquete Python.
│   ├── main.py                  # Crea la app FastAPI, registra routers y crea tablas.
│   ├── database.py              # Configura engine, sesión SQLAlchemy y dependencia get_db.
│   ├── models/                  # Modelos ORM (tablas de MySQL).
│   │   ├── __init__.py
│   │   ├── shipment.py          # Modelo Shipment, enum de estados y transiciones.
│   │   └── tracking.py          # Modelo TrackingEvent (historial).
│   ├── schemas/                 # Esquemas Pydantic (validación entrada/salida).
│   │   ├── __init__.py
│   │   ├── shipment.py
│   │   └── tracking.py
│   ├── routers/                 # Endpoints HTTP (capa API).
│   │   ├── __init__.py
│   │   ├── shipments.py
│   │   └── tracking.py
│   └── services/                # Lógica de negocio y acceso a datos.
│       ├── __init__.py
│       ├── shipment_service.py
│       └── tracking_service.py
├── tests/
│   ├── conftest.py              # Fixtures de Pytest y BD de pruebas.
│   ├── test_shipments.py        # Pruebas del módulo de envíos.
│   └── test_tracking.py         # Pruebas de trazabilidad.
├── .env                         # Variables de entorno locales (no se versiona).
├── .env.example                 # Plantilla de variables de entorno.
├── .gitignore
├── requirements.txt
├── README.md
└── run.py                       # Ejecuta Uvicorn para desarrollo.
```

### Diferencia rápida entre capas

- **Modelos (models)**: representan tablas en MySQL con SQLAlchemy.
- **Esquemas (schemas)**: validan y dan forma a los datos que entran/salen por la API con Pydantic.
- **Servicios (services)**: contienen reglas de negocio, como validar transiciones de estado.
- **Routers (routers)**: reciben peticiones HTTP, llaman servicios y devuelven respuestas.

## 12. Explicación del flujo de una petición HTTP

Ejemplo: `PATCH /api/v1/shipments/1/status`

1. **Cliente** envía una petición HTTP con JSON.
2. **FastAPI/Router** (`app/routers/shipments.py`) recibe la ruta y valida el cuerpo usando el esquema Pydantic `ShipmentStatusUpdate`.
3. **Dependencia `get_db`** (`app/database.py`) crea una sesión SQLAlchemy para esa petición.
4. **Servicio** (`app/services/shipment_service.py`) ejecuta la lógica: busca el envío, valida la transición, actualiza estado y crea un `TrackingEvent`.
5. **SQLAlchemy** traduce operaciones Python a SQL y confirma la transacción en MySQL.
6. **Respuesta** se serializa con `ShipmentResponse` y FastAPI devuelve JSON con el código HTTP apropiado (200, 404, 409, etc.).
7. **Cierre de sesión**: `get_db` cierra la sesión en el `finally`.

## 13. Endpoints principales

### Envíos

- `POST /api/v1/shipments` — Crear envío (201).
- `GET /api/v1/shipments?page=1&page_size=10` — Listar envíos paginados (200).
- `GET /api/v1/shipments/{shipment_id}` — Consultar por ID (200/404).
- `GET /api/v1/shipments/tracking/{tracking_number}` — Consultar por guía (200/404).
- `PUT /api/v1/shipments/{shipment_id}` — Actualizar envío (200/404/409).
- `PATCH /api/v1/shipments/{shipment_id}/status` — Cambiar estado (200/404/409).
- `DELETE /api/v1/shipments/{shipment_id}` — Cancelar envío (204/404/409).

### Trazabilidad

- `GET /api/v1/shipments/{shipment_id}/tracking` — Historial por ID (200/404).
- `GET /api/v1/tracking/{tracking_number}` — Historial por guía (200/404).

## 14. Reglas de transición de estados

- `PENDING` -> `PICKED_UP`, `CANCELLED`
- `PICKED_UP` -> `IN_TRANSIT`, `CANCELLED`
- `IN_TRANSIT` -> `OUT_FOR_DELIVERY`, `CANCELLED`
- `OUT_FOR_DELIVERY` -> `DELIVERED`, `CANCELLED`
- `DELIVERED` -> sin transiciones
- `CANCELLED` -> sin transiciones

Cualquier transición no permitida responde con `409 Conflict`.
