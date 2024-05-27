from typing import List

from sqlmodel import create_engine, SQLModel, Session, select
import uvicorn
from fastapi import FastAPI, HTTPException, Depends

from schemas import WorkerInput, WorkerOutput, JobInput, JobOutput, Worker, Job

app = FastAPI(title="Recruitment Info")

# database creation (change from sqlite to PostgreSQL or whatever)
engine = create_engine(
    "sqlite:///recruitment.db",
    connect_args={"check_same_thread": False},
    echo=True,
)

# start function
@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)

# creating session and using dependency injection to use it in every request
# instead of return I use generator function and yield which could act like an iterator
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/api/workers")
async def get_workers(age: int = None, profession: str = None,
                      session: Session = Depends(get_session)) -> List[WorkerOutput]:
    query = select(Worker)
    if age:
        query = query.where(Worker.age == age)
    if profession:
        query = query.where(Worker.profession == profession)
    return session.exec(query).all()

@app.get("/api/workers/{id}", response_model=Worker)
async def worker_by_id(id: int, session: Session = Depends(get_session)) -> Worker:
    worker = session.get(Worker, id)
    if worker:
        return worker
    else:
        raise HTTPException(status_code=404, detail=f"Worker with id {id} is not found")

@app.post("/api/workers/", response_model=Worker)
async def add_worker(worker_input: WorkerInput,
                     session: Session = Depends(get_session)) -> Worker:
    new_worker = Worker.from_orm(worker_input)
    session.add(new_worker)
    session.commit()
    session.refresh(new_worker)
    return new_worker

@app.delete("/api/workers/{id}", status_code=204)
async def delete_worker(id: int, session: Session = Depends(get_session)) -> None:
    worker = session.get(Worker, id)
    if worker:
        session.delete(worker)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No Worker with id={id}")

@app.put("/api/workers/{id}", response_model=Worker)
async def update_worker(id: int, new_data: WorkerInput,
                        session: Session = Depends(get_session)) -> Worker:
    worker = session.get(Worker, id)
    if worker is not None:
        worker.profession = new_data.profession
        worker.age = new_data.age
        worker.name = new_data.name
        session.commit()
        return worker
    else:
        raise HTTPException(status_code=404, detail=f"No Worker with id={id}")

@app.post("/api/jobs", response_model=Job)
async def add_job(worker_ids: List[int], job_input: JobInput,
                  session: Session = Depends(get_session)) -> Job:
    employees = []
    for worker_id in worker_ids:
        worker = session.get(Worker, worker_id)
        if worker:
            employees.append(worker)

    new_job = Job.from_orm(job_input, update={"worker_ids":worker_ids})
    new_job.workers = employees
    session.add(new_job)
    session.commit()
    session.refresh(new_job)
    return new_job

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
