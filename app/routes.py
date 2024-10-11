from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import logging
import csv
import io
from . import crud, schemas
from .database import get_db

# Configurar el logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(
    employees_file: UploadFile = File(...),
    departments_file: UploadFile = File(...),
    jobs_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        logger.info("Processing CSV upload...")

        # Procesar departamentos
        departments_data = csv.reader(io.StringIO(departments_file.file.read().decode('utf-8')))
        for row in departments_data:
            if not row[0] or not row[1]:
                logger.error(f"Missing data in department row: {row}. Inserting with null values.")
                # Aquí decides si quieres insertar con valores por defecto o `None`
                crud.create_department(db, schemas.DepartmentCreate(department=row[1] or None))
            else:
                logger.info(f"Processing department: {row}")
                crud.create_department(db, schemas.DepartmentCreate(department=row[1]))

        # Procesar trabajos
        jobs_data = csv.reader(io.StringIO(jobs_file.file.read().decode('utf-8')))
        for row in jobs_data:
            if not row[0] or not row[1]:
                logger.error(f"Missing data in job row: {row}. Inserting with null values.")
                crud.create_job(db, schemas.JobCreate(job=row[1] or None))
            else:
                logger.info(f"Processing job: {row}")
                crud.create_job(db, schemas.JobCreate(job=row[1]))

        # Procesar empleados
        employees_data = csv.reader(io.StringIO(employees_file.file.read().decode('utf-8')))
        for row in employees_data:
            logger.info(f"Processing employee: {row}")
            
            # Si faltan valores, asignar `None` en lugar de omitir la fila
            name = row[1] or None
            datetime = row[2] or None
            department_id = int(row[3]) if row[3] else None
            job_id = int(row[4]) if row[4] else None

            crud.create_employee(db, schemas.EmployeeCreate(
                name=name,
                datetime=datetime,
                department_id=department_id,
                job_id=job_id
            ))

        logger.info("CSV data uploaded successfully")
        return {"message": "CSV data uploaded successfully"}

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")




# Endpoint para la inserción de empleados en lotes
@router.post("/batch-insert-employees/")
async def batch_insert_employees(batch: schemas.EmployeeBatchCreate, db: Session = Depends(get_db)):
    try:
        if len(batch.employees) > 1000:
            logger.warning("Tried to insert more than 1000 employees.")
            raise HTTPException(status_code=400, detail="Cannot insert more than 1000 employees at once.")

        logger.info(f"Inserting batch of {len(batch.employees)} employees.")
        crud.create_employees_batch(db=db, employees=batch)
        logger.info("Batch inserted successfully")
        return {"message": f"{len(batch.employees)} employees inserted successfully"}

    except Exception as e:
        logger.error(f"An error occurred during batch insert: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
