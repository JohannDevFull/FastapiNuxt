"""Configuración compartida para pruebas con Pytest.

Conceptos clave:
- Fixture: función que Pytest puede inyectar en las pruebas para preparar
  datos o recursos (como una base de datos de prueba).
- TestClient: cliente de FastAPI que permite hacer peticiones HTTP a la app
  sin levantar un servidor real.
- dependency_overrides: mecanismo de FastAPI para reemplazar una dependencia
  (como get_db) durante las pruebas.

IMPORTANTE: estas pruebas usan la base de datos minicargoflow_test, definida
en .env o por defecto en este archivo. No usan la base de datos de desarrollo.
"""

import os
import sys
from pathlib import Path

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Aseguramos que la carpeta raíz del proyecto esté en el path de importación.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

# Usamos una base de datos separada para pruebas.
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL_TEST",
    "mysql+pymysql://root:@127.0.0.1:3306/minicargoflow_test",
)

# Verificación de seguridad: evitamos ejecutar pruebas contra una BD que no parezca de test.
if "test" not in TEST_DATABASE_URL.lower():
    raise RuntimeError("La URL de base de datos de pruebas debe contener 'test' en el nombre.")

test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Importamos la app y metadatos después de preparar el entorno de pruebas.
from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models import shipment, tracking  # noqa: F401,E402


@pytest.fixture(scope="function")
def db_session():
    """Crea un esquema limpio para cada prueba.

    Se eliminan y recrean las tablas antes de cada test para asegurar
    aislamiento: una prueba no depende de datos dejados por otra.
    """
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(db_session):
    """Crea un TestClient que usa la sesión de base de datos de pruebas."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Reemplazamos la dependencia get_db por la versión de prueba.
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
