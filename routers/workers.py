from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from db import get_session
from schemas import WorkerOutput, Worker, WorkerInput, Job, JobInput

router = APIRouter(prefix="/api")

@router.get("/workers")
async def get_workers(age: int = None, profession: str = None,
                      session: Session = Depends(get_session)) -> List[WorkerOutput]:
    query = select(Worker)
    if age:
        query = query.where(Worker.age == age)
    if profession:
        query = query.where(Worker.profession == profession)
    return session.exec(query).all()


@router.get("/workers/{id}", response_model=Worker)
async def worker_by_id(id: int, session: Session = Depends(get_session)) -> Worker:
    worker = session.get(Worker, id)
    if worker:
        return worker
    else:
        raise HTTPException(status_code=404, detail=f"Worker with id {id} is not found")


@router.post("/workers/", response_model=Worker)
async def add_worker(worker_input: WorkerInput,
                     session: Session = Depends(get_session)) -> Worker:
    new_worker = Worker.from_orm(worker_input)
    session.add(new_worker)
    session.commit()
    session.refresh(new_worker)
    return new_worker


@router.delete("/workers/{id}", status_code=204)
async def delete_worker(id: int, session: Session = Depends(get_session)) -> None:
    worker = session.get(Worker, id)
    if worker:
        session.delete(worker)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No Worker with id={id}")


@router.put("/workers/{id}", response_model=Worker)
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


class BadJobException(Exception):
    pass


@router.post("/jobs", response_model=Job)
async def add_job(worker_ids: List[int], job_input: JobInput,
                  session: Session = Depends(get_session)) -> Job:
    employees = []
    for worker_id in worker_ids:
        worker = session.get(Worker, worker_id)
        if worker:
            employees.append(worker)

    new_job = Job.from_orm(job_input, update={"worker_ids":worker_ids})
    if new_job.end_date < new_job.start_date:
        raise BadJobException("Job ended before start date")
    new_job.workers = employees
    session.add(new_job)
    session.commit()
    session.refresh(new_job)
    return new_job
