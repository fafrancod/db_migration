from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
import logging
import csv
import io
from . import crud, schemas, models
from sqlalchemy import text
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

@router.get("/employees-hired-by-quarter/")
def employees_hired_by_quarter(db: Session = Depends(get_db)):
    query = text("""
    SELECT d.department AS department, j.job AS job,
    SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(COALESCE(e.datetime, '1900-01-01') AS TIMESTAMP)) = 1 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(COALESCE(e.datetime, '1900-01-01') AS TIMESTAMP)) = 2 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(COALESCE(e.datetime, '1900-01-01') AS TIMESTAMP)) = 3 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN EXTRACT(QUARTER FROM CAST(COALESCE(e.datetime, '1900-01-01') AS TIMESTAMP)) = 4 THEN 1 ELSE 0 END) AS Q4
    FROM employees e
    LEFT JOIN departments d ON e.department_id = d.id
    LEFT JOIN jobs j ON e.job_id = j.id
    WHERE EXTRACT(YEAR FROM CAST(COALESCE(e.datetime, '1900-01-01') AS TIMESTAMP)) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department ASC, j.job ASC;
    """)
    try:
        result = db.execute(query).fetchall()
        
        if not result:
            raise HTTPException(status_code=404, detail="No data found for 2021")
        # Convertir los resultados en una lista de diccionarios para que FastAPI pueda serializarlos
        response = []
        for row in result:
            response.append({
                "department": row[0],
                "job": row[1],
                "Q1": row[2],
                "Q2": row[3],
                "Q3": row[4],
                "Q4": row[5]
            })
        return response
    except Exception as e:
        logger.error(f"An error occurred during the query execution: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/departments-hiring-above-average/")
def departments_hiring_above_average(db: Session = Depends(get_db)):
    query = text("""
    WITH department_hires AS (
        SELECT d.id, d.department, COUNT(e.id) AS hired
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE EXTRACT(YEAR FROM CAST(COALESCE(e.datetime, '1900-01-01') AS TIMESTAMP)) = 2021
        GROUP BY d.id, d.department
    )

    SELECT id, department, hired
    FROM department_hires
    WHERE hired > (SELECT AVG(hired) FROM department_hires)
    ORDER BY hired DESC;
    """)
    try:
        result = db.execute(query).fetchall()
        
        # Mostrar los resultados en la consola
        if not result:
            logger.info("No departments found hiring above average.")
            raise HTTPException(status_code=404, detail="No departments found hiring above average")
        
        # Convertir el resultado en una lista de diccionarios para que sea legible
        result_dicts = [{"id": row[0], "department": row[1], "hired": row[2]} for row in result]
        
        # Imprimir el resultado en la consola
        logger.info(f"Departments hiring above average: {result_dicts}")
        
        return result_dicts
    
    except Exception as e:
        logger.error(f"An error occurred during the query execution: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


