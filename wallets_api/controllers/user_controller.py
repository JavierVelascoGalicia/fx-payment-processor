from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from wallets_api.database import get_db_session
from wallets_api.schemas.user import UserRequest, UserResponse
from wallets_api.schemas.generic import GenericResponse
from wallets_api.services.users_service import UserService
from wallets_api.utils.utils import Utils


user_controller = APIRouter(prefix="/users", tags=["users"])


@user_controller.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserRequest, session: Session = Depends(get_db_session)) -> UserResponse:
    user = await UserService.create_user(user, session)
    return user


@user_controller.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: str, session: Session = Depends(get_db_session)) -> UserResponse:
    user = await UserService.get_user_by_id(user_id, session)
    return user


@user_controller.delete("/{user_id}", response_model=GenericResponse)
async def get_delete_user(user_id: str, session: Session = Depends(get_db_session)) -> GenericResponse:
    response = await UserService.delete_user(user_id, session)
    return response
