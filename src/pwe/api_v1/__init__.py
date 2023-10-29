from fastapi import APIRouter

from . import todo
from . import user

router = APIRouter(prefix='/v1')
router.include_router(router=todo.router)
router.include_router(router=user.router)
