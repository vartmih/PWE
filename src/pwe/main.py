import uvicorn
from fastapi import FastAPI, APIRouter

from pwe import api_v1
from pwe.settings import settings

app = FastAPI(
    title='PWE',
    debug=settings.debug,
)

top_router = APIRouter(prefix='/api')
top_router.include_router(api_v1.router)

app.include_router(top_router)

if __name__ == "__main__":
    uvicorn.run(
        "pwe.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
