
from wallets_api.schemas.user import UserRequest, UserResponse
from wallets_api.schemas.generic import GenericResponse
from wallets_api.utils.utils import Utils

from wallets_api.models.models import User
from wallets_api.services.wallets_service import WalletService

from sqlmodel import Session


class UserService:

    @staticmethod
    async def create_user(user: UserRequest, session: Session) -> UserResponse:
        user = User(user_id=user.user_id)
        session.add(user)
        session.commit()
        await WalletService.create_wallet(str(user.user_id), "USD", session)
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

        user.is_deleted = True
        session.add(user)
        session.commit()
        return GenericResponse(status="OK", detail="User deleted")
