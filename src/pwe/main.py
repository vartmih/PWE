import uvicorn
from fastapi import FastAPI, APIRouter

from pwe import api_v1
from pwe.settings import settings


app = FastAPI(
    title='PWE',
    debug=settings.DEBUG,
)

top_router = APIRouter(prefix='/api')
top_router.include_router(api_v1.router)

app.include_router(top_router)


if __name__ == "__main__":
    print(f'Running on {settings.SERVER_HOST}:{settings.SERVER_PORT}')
    uvicorn.run(
        app="main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True
    )
