from datetime import date
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship

class JobInput(SQLModel):
    title: str
    salary: float
    description: str
    location: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class WorkerInput(SQLModel):
    name: str
    age: Optional[int] = None
    profession: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Alex",
                "age": 23,
                "profession": "Programmer"
            }
        }

class Worker(WorkerInput, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="job.id")
    job: Optional["Job"] = Relationship(back_populates="workers")

class WorkerOutput(WorkerInput):
    id: int

class JobOutput(JobInput):
    id: int
    employees: List[WorkerOutput] = []

class Job(JobInput, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workers: List[Worker] = Relationship(back_populates="job")
