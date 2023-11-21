import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from pwe.api_v1.user.auth import auth_backend
from pwe.api_v1.user.manager import get_user_manager
from pwe.api_v1.user.models import User
from pwe.api_v1.user.schemas import UserCreateSchema, UserSchema, UserUpdateSchema

router = APIRouter(prefix="/users", tags=["Пользователь"])

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

router.include_router(fastapi_users.get_register_router(UserSchema, UserCreateSchema))
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_users_router(UserSchema, UserUpdateSchema))
