"""Permite ejecutar la aplicación con: python run.py

Uvicorn es el servidor ASGI que ejecuta aplicaciones FastAPI.
El parámetro reload=True recarga la app al detectar cambios (útil en desarrollo).
"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
