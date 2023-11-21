from fastapi import APIRouter

from pwe.api_v1 import todo
from pwe.api_v1 import user

router = APIRouter(prefix='/v1')
router.include_router(router=todo.router)
router.include_router(router=user.router)
