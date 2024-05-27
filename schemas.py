import json

from pydantic import BaseModel

class WorkerInput(BaseModel):
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

class WorkerOutput(WorkerInput):
    id: int




def load_db()-> list[WorkerOutput]:
    """Load a list of workers from a JSON file"""
    with open('workers.json') as file:
        return [WorkerOutput.parse_obj(obj) for obj in json.load(file)]

def save_db(workers: list[WorkerOutput]):
    with open('workers.json', 'w') as file:
        json.dump([worker.dict() for worker in workers], file, indent=4)