import uvicorn

from fastapi import FastAPI

from pwe.api_v1 import todo
from pwe.settings import settings

app = FastAPI()

app.include_router(todo.views.router)

if __name__ == "__main__":
    uvicorn.run(
        "pwe.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
