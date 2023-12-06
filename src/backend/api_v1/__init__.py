from fastapi import APIRouter

from backend.api_v1 import todo
from backend.api_v1 import user

router = APIRouter(prefix='/v1')
router.include_router(router=todo.router)
router.include_router(router=user.router)
