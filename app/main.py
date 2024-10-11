import logging
from fastapi import FastAPI
from .database import engine
from . import models
from .routes import router as api_router

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
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
