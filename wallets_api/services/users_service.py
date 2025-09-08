
from wallets_api.schemas.user import UserRequest, UserResponse
from wallets_api.schemas.generic import GenericResponse
from wallets_api.utils.utils import Utils

from wallets_api.models.models import User
from wallets_api.models.models import Wallet

from sqlmodel import Session
from datetime import datetime


class UserService:

    @staticmethod
    async def create_user(user: UserRequest, session: Session) -> UserResponse:
        user = User(user_id=user.user_id)
        wallet = Wallet(user_id=user.user_id, currency="USD")
        session.add(user)
        session.add(wallet)
        session.commit()

        session.refresh(user)
        return UserResponse(**user.model_dump())

    @staticmethod
    async def get_user_by_id(user_id: str, session: Session) -> User:
        user = session.get(User, user_id)
        await Utils.validate_response(user)
        await Utils.validate_deleted(user)

        return user

    @staticmethod
    async def delete_user(user_id: str, session: Session) -> GenericResponse:
        # Soft delete
        user = await UserService.get_user_by_id(user_id, session)

        user.deleted_at = datetime.now()
        session.add(user)
        session.commit()
        return GenericResponse(status="OK", detail="User deleted")
