
from fastapi import HTTPException


class Utils:

    @staticmethod
    async def validate_response(object):
        if not object:
            raise HTTPException(status_code=404, detail="Resource not found")

    @staticmethod
    async def validate_deleted(object):
        if object.is_deleted:
            raise HTTPException(status_code=500, detail="User already deleted")
