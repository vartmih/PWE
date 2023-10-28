from fastapi import APIRouter

from .todo import views

router = APIRouter(prefix='/v1')
router.include_router(router=views.router)
