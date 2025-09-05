
from wallets_api.schemas.user import UserRequest, UserResponse
from wallets_api.schemas.generic import GenericResponse
from wallets_api.utils.utils import Utils

from fastapi import HTTPException

from wallets_api.models.models import User

from sqlmodel import Session

class UserService:

    @staticmethod
    async def create_user(user: UserRequest, session: Session) -> UserResponse:
        user = User(user_id=user.user_id)
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserResponse(**user.model_dump())

    @staticmethod
    async def get_user_by_id(user_id: str, session: Session) -> UserResponse:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(**user.model_dump())

    @staticmethod
    async def delete_user(user_id: str, session: Session) -> GenericResponse:
        # Soft delete
        user = session.get(User, user_id)

        await Utils.validate_deleted(user)

        session.add(user)
        session.commit()
        return GenericResponse(status="OK", detail="User deleted")
