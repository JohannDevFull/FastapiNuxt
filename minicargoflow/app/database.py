"""Configuración de la conexión a la base de datos.

Este archivo centraliza la creación del motor (engine) de SQLAlchemy,
la sesión de base de datos y la clase base para los modelos ORM.

Conceptos clave:
- Engine: objeto que sabe cómo conectarse a la base de datos.
- Session: representa una "conversación" con la base de datos; permite
  consultar, insertar, actualizar y eliminar registros.
- Declarative Base: clase base de la que heredan los modelos ORM.
- Depends (FastAPI): mecanismo de inyección de dependencias; FastAPI
  ejecuta una función dependiente y pasa su resultado al endpoint.
"""

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Cargamos las variables definidas en el archivo .env.
# Esto permite mantener credenciales fuera del código fuente.
load_dotenv()

# Leemos la URL de conexión desde variables de entorno.
# Si no existe, usamos un valor por defecto para desarrollo local con Laragon.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@127.0.0.1:3306/minicargoflow",
)

# Creamos el engine de SQLAlchemy.
# echo=False evita imprimir todas las consultas SQL en consola.
# pool_pre_ping=True verifica que la conexión siga viva antes de usarla.
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# sessionmaker crea una "fábrica" de sesiones.
# autocommit=False: los cambios se confirman manualmente con commit().
# autoflush=False: evitamos envíos automáticos antes de tiempo.
# bind=engine: indica qué conexión de base de datos usarán las sesiones.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Clase base para todos los modelos ORM.

    Los modelos (tablas) heredan de esta clase para que SQLAlchemy
    pueda registrar sus columnas y metadatos.
    """

    pass


def get_db() -> Generator[Session, None, None]:
    """Proporciona una sesión de base de datos por petición HTTP.

    Esta función se usa con Depends() en FastAPI. FastAPI la ejecuta
    antes del endpoint, entrega la sesión (yield) y, al finalizar,
    ejecuta el bloque finally para cerrar la sesión.

    El patrón yield/finally garantiza que la sesión se cierre aunque
    ocurra un error durante la petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
