from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Modelo para la tabla Department
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)

    # Relación con empleados (Un departamento tiene muchos empleados)
    employees = relationship("Employee", back_populates="department")


# Modelo para la tabla Job
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, index=True)

    # Relación con empleados (Un trabajo puede tener muchos empleados)
    employees = relationship("Employee", back_populates="job")


# Modelo para la tabla Employee
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    datetime = Column(String, nullable=True)

    # Clave foránea que se relaciona con el ID de la tabla Department
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    # Clave foránea que se relaciona con el ID de la tabla Job
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)

    # Relación con el modelo Department (Un empleado pertenece a un departamento)
    department = relationship("Department", back_populates="employees")

    # Relación con el modelo Job (Un empleado tiene un trabajo específico)
    job = relationship("Job", back_populates="employees")
