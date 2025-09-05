
from wallets_api.models.models import User
from fastapi import HTTPException


class Utils:

    @staticmethod
    async def validate_deleted(user: User):
        if user.is_deleted:
            raise HTTPException(status_code=500, detail="User already deleted")
