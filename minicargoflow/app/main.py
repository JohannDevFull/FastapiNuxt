"""Punto de entrada principal de la aplicación FastAPI.

Aquí se crea la instancia de FastAPI, se registran los routers
y se crean las tablas en la base de datos al iniciar.

Conceptos clave:
- FastAPI(): crea la aplicación web.
- Decorador @app.on_event("startup"): ejecuta una función cuando
  la aplicación inicia.
- include_router(): conecta rutas definidas en otros archivos.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Importamos los modelos para que SQLAlchemy los registre en Base.metadata
# antes de crear las tablas. Sin estas importaciones, create_all no sabría
# qué tablas debe crear.
from app.models import shipment, tracking  # noqa: F401
from app.routers import shipments, tracking as tracking_router

# Creamos la instancia principal de la aplicación.
# title, description y version aparecen en la documentación Swagger (/docs).
app = FastAPI(
    title="Mini CargoFlow",
    description="API educativa para gestión y seguimiento de envíos.",
    version="1.0.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")

def create_database_tables() -> None:
    """Crea las tablas en la base de datos al iniciar la aplicación.

    SQLAlchemy revisa los modelos registrados en Base.metadata y crea
    las tablas que no existan. Esta decisión es adecuada para la V1
    educativa; en una evolución futura se puede usar Alembic para
    manejar migraciones de forma controlada.
    """
    Base.metadata.create_all(bind=engine)


# Registramos los routers. Cada router agrupa endpoints relacionados.
app.include_router(shipments.router)
app.include_router(tracking_router.router)


@app.get("/", tags=["Health"])
def read_root() -> dict:
    """Endpoint simple para verificar que la API está funcionando."""
    return {"message": "Mini CargoFlow API está en ejecución"}
