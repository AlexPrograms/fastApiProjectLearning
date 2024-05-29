from datetime import date
from typing import List, Optional

from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, Relationship, Column, VARCHAR

pwd_context = CryptContext(schemes=["bcrypt"])
class UserOutput(SQLModel):
    id: int
    username: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(sa_column=Column("username", VARCHAR, unique=True, index=True))
    password_hash: str = ""

    def set_password(self, password):
        """Setting the paswords actually sets the password_hash"""
        self.password_hash=pwd_context.hash(password)

    def verify_password(self, password):
        """Verify given password by hashing and comparing to password_hash"""
        return pwd_context.verify(password, self.password_hash)



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
