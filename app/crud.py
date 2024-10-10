from sqlalchemy.orm import Session
from . import models, schemas

def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(department=department.department)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(job=job.job)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(
        name=employee.name,
        datetime=employee.datetime,
        department_id=employee.department_id,
        job_id=employee.job_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def create_employees_batch(db: Session, employees: schemas.EmployeeBatchCreate):
    for employee in employees.employees:
        create_employee(db, employee)
