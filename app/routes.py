from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import logging
import csv
import io
from . import crud, schemas, models  # Asegúrate de importar models
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
        next(departments_data)  # Saltar la cabecera si tiene una
        department_ids = set()  # Almacenar los IDs de departamentos insertados
        for row in departments_data:
            department_id = int(row[0]) if row[0] else None
            department_name = row[1] if row[1] else None
            if department_id and department_name:
                logger.info(f"Inserting department: {row}")
                db_department = models.Department(id=department_id, department=department_name)  # Modificación aquí para que se asigne el ID
                db.add(db_department)
                department_ids.add(department_id)  # Añadir a la lista de IDs insertados
            else:
                logger.error(f"Invalid department data: {row}. Skipping.")

        # Confirmar que los departamentos fueron insertados
        db.commit()

        # Verificar si hay departamentos cargados
        all_departments = db.query(models.Department).all() 
        logger.info(f"Departments in the database: {all_departments}")

        if not department_ids:
            raise HTTPException(status_code=400, detail="No departments were uploaded. Aborting.")

        # Procesar trabajos
        jobs_data = csv.reader(io.StringIO(jobs_file.file.read().decode('utf-8')))
        next(jobs_data)  # Saltar la cabecera si tiene una
        job_ids = set()  # Almacenar los IDs de trabajos insertados
        for row in jobs_data:
            job_id = int(row[0]) if row[0] else None
            job_title = row[1] if row[1] else None
            if job_id and job_title:
                logger.info(f"Inserting job: {row}")
                db_job = models.Job(id=job_id, job=job_title)  # Modificación aquí para que se asigne el ID
                db.add(db_job)
                job_ids.add(job_id)
            else:
                logger.error(f"Invalid job data: {row}. Skipping.")

        # Confirmar que los trabajos fueron insertados
        db.commit()

        # Procesar empleados
        employees_data = csv.reader(io.StringIO(employees_file.file.read().decode('utf-8')))
        next(employees_data)  # Saltar la cabecera si tiene una
        for row in employees_data:
            name = row[1] if row[1] else None
            datetime = row[2] if row[2] else None
            department_id = int(row[3]) if row[3] else None
            job_id = int(row[4]) if row[4] else None

            # Validar que el department_id y job_id existen
            if department_id and department_id not in department_ids:
                logger.error(f"Department ID {department_id} not found for employee: {row}. Skipping.")
                continue
            if job_id and job_id not in job_ids:
                logger.error(f"Job ID {job_id} not found for employee: {row}. Skipping.")
                continue

            logger.info(f"Inserting employee: {row}")
            db_employee = models.Employee(
                name=name,
                datetime=datetime,
                department_id=department_id,
                job_id=job_id
            )
            db.add(db_employee)

        # Confirmar la inserción de empleados
        db.commit()

        logger.info("CSV data uploaded successfully")
        return {"message": "CSV data uploaded successfully"}

    except Exception as e:
        db.rollback()  # Revertir los cambios en caso de error
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


# Obtener todos los departamentos
@router.get("/departments/")
def get_departments(db: Session = Depends(get_db)):
    departments = db.query(models.Department).all()
    if not departments:
        raise HTTPException(status_code=404, detail="No departments found")
    return departments

# Obtener todos los trabajos
@router.get("/jobs/")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    if not jobs:
        raise HTTPException(status_code=404, detail="No jobs found")
    return jobs

# Obtener todos los empleados
@router.get("/employees/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found")
    return employees