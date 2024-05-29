from http import HTTPStatus
from sqlmodel import SQLModel
import uvicorn
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from db import engine
from routers import workers, web, auth
from routers.workers import BadJobException

app = FastAPI(title="Recruitment Info")
app.include_router(workers.router)
app.include_router(web.router)
app.include_router(auth.router)



# start function
@app.on_event("startup")
def startup():
    SQLModel.metadata.create_all(engine)

@app.exception_handler(BadJobException)
async def uvicorn_exception_handler(request: Request, exc: BadJobException):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Bad Job"},
    )

@app.middleware("http")
async def add_workers_cookes(request: Request, call_next):
    response = await call_next(request)
    response.set_cookie(key="workers_cookie", value="you_visited_recruitment_CRM_and_got_scammed)")
    return response

# These are old notes, before refactoring
# creating session and using dependency injection to use it in every request
# instead of return I use generator function and yield which could act like an iterator

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
