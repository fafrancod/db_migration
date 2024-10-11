from pydantic import BaseModel
from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel




class DepartmentCreate(BaseModel):
    department: str

class JobCreate(BaseModel):
    job: str

class EmployeeCreate(BaseModel):
    name: Optional[str] = None
    datetime: Optional[str] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None


class EmployeeBatchCreate(BaseModel):
    employees: List[EmployeeCreate]
