from pathlib import Path

import uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pwe import api_v1
from pwe.settings import settings
from pwe.utils import get_app_info, get_version_app

static_dir = Path(__file__).parent / 'static'

app = FastAPI(
    title='PWE',
    debug=settings.DEBUG,
)

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory=f"{static_dir}"), name="static")
templates = Jinja2Templates(directory=f"{static_dir}/templates")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request):
    """
    Главная страница

    Parameters:
        request: запрос

    :return: HTML страница
    """
    app_info = get_app_info()
    app_version = get_version_app()
    return templates.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "app_info": app_info,
            "app_version": app_version
        })


top_router = APIRouter(prefix='/api')
top_router.include_router(api_v1.router)

app.include_router(top_router)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
