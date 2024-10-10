from pydantic import BaseModel
from datetime import datetime
from typing import List

class DepartmentCreate(BaseModel):
    department: str

class JobCreate(BaseModel):
    job: str

class EmployeeCreate(BaseModel):
    name: str
    datetime: datetime
    department_id: int
    job_id: int

class EmployeeBatchCreate(BaseModel):
    employees: List[EmployeeCreate]
