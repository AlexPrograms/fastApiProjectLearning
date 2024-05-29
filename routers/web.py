from fastapi import APIRouter, Request, Form, Depends
from sqlmodel import Session
from db import get_session
from routers.workers import get_workers
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

templates = Jinja2Templates(directory="templates")
@router.get('/', response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse('home.html',
                                      {'request': request})

@router.post("/search", response_class=HTMLResponse)
async def search(*, age:int = Form(...),
                 profession: str = Form(...),
                 request: Request,
                 session: Session = Depends(get_session)):
    workers = await get_workers(age=age, profession=profession, session=session)
    return templates.TemplateResponse('search_results.html',
                                      {'request': request, 'workers': workers})
