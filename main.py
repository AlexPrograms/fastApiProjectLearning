from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, save_db, WorkerInput, WorkerOutput

app = FastAPI(title="Rectuitment Info")

db = load_db()

@app.get("/api/workers")
async def get_workers(age:int|None=None, profession:str|None=None) -> List:
    result = db
    if age is not None:
        result = [worker for worker in result if worker.age == age]
    if profession is not None:
        result = [worker for worker in result if worker.profession.lower() == profession.lower()]
    return result
@app.get("/api/workers/{id}")
async def worker_by_id(id:int):
    result = [worker for worker in db if worker.id == id]
    if result is not None:
        return result
    else:
        raise HTTPException(status_code=404, detail="No Worker Found")

@app.post("/api/workers/", response_model=WorkerOutput)
async def add_worker(worker: WorkerInput) -> WorkerOutput:
    new_worker = WorkerOutput(name=worker.name, age=worker.age,
                              profession=worker.profession, id=len(db)+1)
    db.append(new_worker)
    save_db(db)
    return new_worker


@app.delete("/api/workers/{id}", status_code=204)
async def delete_worker(id:int)->None:
    matches = [worker for worker in db if worker.id == id]
    if matches is not None:
        worker = matches[0]
        db.remove(worker)
        save_db(db)
    else:
        raise HTTPException(status_code=404,
                            detail=f"No Worker with id={id}Found")

@app.put("/api/workers/{id}", response_model=WorkerOutput)
async def update_worker(id:int, new_data: WorkerInput) -> WorkerOutput:
    matches = [worker for worker in db if worker.id == id]
    if matches is not None:
        worker = matches[0]
        worker.age = new_data.age
        worker.profession = new_data.profession
        worker.name = new_data.name
        save_db(db)
        return worker
    else:
        raise HTTPException(status_code=404, detail=f"No Worker with id={id}")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)