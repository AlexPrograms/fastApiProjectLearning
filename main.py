from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

db = [
    {"id": 1, "name": "Anna", "age": 25, "profession": "Cleaner"},
{"id": 2, "name": "Konstantin", "age": 25, "profession": "Rectuiter"},
{"id": 3, "name": "Julia", "age": 30, "profession": "Teacher"},
{"id": 4, "name": "Vlad", "age": 66, "profession": "Manager"},
{"id": 5, "name": "Danny", "age": 32, "profession": "Bloger"},
{"id": 6, "name": "Tommy", "age": 21, "profession": "Youtuber"}
]

@app.get("/api/workers")
async def get_workers(age:int|None=None, profession:str|None=None) -> List:
    result = db
    if age is not None:
        result = [worker for worker in result if worker["age"] == age]
    if profession is not None:
        result = [worker for worker in result if worker["profession"].lower() == profession.lower()]
    return result
@app.get("/api/workers/{id}")
async def car_by_id(id:int) -> dict:
    result = [worker for worker in db if worker["id"] == id]
    if result is not None:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail="No Worker Found")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)