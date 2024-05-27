from typing import List


from sqlmodel import create_engine, SQLModel, Session
import uvicorn
from fastapi import FastAPI, HTTPException

from schemas import load_db, save_db, WorkerInput, WorkerOutput, JobInput, JobOutput, Worker

app = FastAPI(title="Rectuitment Info")
#json db
db = load_db()
#database creation (change from sqlite to Postgresql or whatever)
engine = create_engine(
    "sqlite:///rectuitment.db",
    connect_args={"check_same_thread": False},
    echo=True,
)


#start function
@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)


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

@app.post("/api/workers/", response_model=Worker)
async def add_worker(worker_input: WorkerInput) -> Worker:
    #creating transaction to execute a bunch of operations together or don't execute anything
    with Session(engine) as session:
        new_worker = Worker.from_orm(worker_input)
        session.add(new_worker)
        session.commit()
        session.refresh(new_worker)
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