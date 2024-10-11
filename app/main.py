import logging
from fastapi import FastAPI, HTTPException
from .database import engine
from app.database import SessionLocal
from . import models
from .routes import router 
from sqlalchemy.orm import Session

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def read_root():
    logger.info("Root endpoint called.")
    return {"message": "API de Migración de Datos está funcionando correctamente"}

# Incluir las rutas de la API
app.include_router(router)  # Ahora es `router`, para que coincida con la definición en `routes.py`

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/test-db-connection")
def test_db_connection():
    db = None
    try:
        # Crear una sesión de base de datos
        db = SessionLocal()
        db.execute("SELECT 1")  # Ejecutar una consulta simple
        return {"message": "Conexión exitosa con la base de datos"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la conexión: {str(e)}")
    finally:
        if db:
            db.close()
