import uvicorn
from fastapi import FastAPI

from pwe.settings import settings

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(
        'pwe.app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
