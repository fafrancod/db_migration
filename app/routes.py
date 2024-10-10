from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import get_db
import csv
import io

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(
    employees_file: UploadFile = File(...),
    departments_file: UploadFile = File(...),
    jobs_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Procesar departamentos
    departments_data = csv.reader(io.StringIO(departments_file.file.read().decode('utf-8')))
    for row in departments_data:
        crud.create_department(db, schemas.DepartmentCreate(department=row[1]))

    # Procesar trabajos
    jobs_data = csv.reader(io.StringIO(jobs_file.file.read().decode('utf-8')))
    for row in jobs_data:
        crud.create_job(db, schemas.JobCreate(job=row[1]))

    # Procesar empleados
    employees_data = csv.reader(io.StringIO(employees_file.file.read().decode('utf-8')))
    for row in employees_data:
        crud.create_employee(db, schemas.EmployeeCreate(
            name=row[1],
            datetime=row[2],
            department_id=int(row[3]),
            job_id=int(row[4])
        ))
    return {"message": "CSV data uploaded successfully"}

@router.post("/batch-insert-employees/")
async def batch_insert_employees(batch: schemas.EmployeeBatchCreate, db: Session = Depends(get_db)):
    if len(batch.employees) > 1000:
        raise HTTPException(status_code=400, detail="Cannot insert more than 1000 employees at once.")
    crud.create_employees_batch(db=db, employees=batch)
    return {"message": f"{len(batch.employees)} employees inserted successfully"}
