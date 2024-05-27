import json
from datetime import date

from sqlmodel import SQLModel, Field, Relationship
#from pydantic import BaseModel


class JobInput(SQLModel):
    title: str
    salary: float
    description: str
    location: str
    start_date: date | None
    end_date: date | None



class WorkerInput(SQLModel):
    name: str
    age: int | None
    profession: str | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Alex",
                "age": 23,
                "profession": "Programmer"
            }
        }

class Worker(WorkerInput, table = True):
    id: int | None = Field(primary_key=True, default=None)

class WorkerOutput(WorkerInput):
    id: int

class JobOutput(JobInput):
    id: int
    employees: list[WorkerOutput]=[]



def load_db()-> list[WorkerOutput]:
    """Load a list of workers from a JSON file"""
    with open('workers.json') as file:
        return [WorkerOutput.parse_obj(obj) for obj in json.load(file)]

def save_db(workers: list[WorkerOutput]):
    with open('workers.json', 'w') as file:
        json.dump([worker.dict() for worker in workers], file, indent=4)