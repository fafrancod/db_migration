from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  
# SQLALCHEMY_DATABASE_URL = "postgresql://<postgres>:<Medal318>@<host>/<mi_base_de_datos>"
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Medal318@localhost:5432/mi_base_de_datos"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Medal318@postgres:5432/mi_base_de_datos"



# Crear la conexión a la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la sesión para la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear el modelo base de SQLAlchemy
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

