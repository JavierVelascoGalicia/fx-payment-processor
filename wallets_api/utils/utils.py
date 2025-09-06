
from fastapi import HTTPException
from wallets_api.utils.enums import CurrencyEnum


class Utils:

    @staticmethod
    async def validate_response(object):
        if not object:
            raise HTTPException(status_code=404, detail="Resource not found")

    @staticmethod
    async def validate_deleted(object):
        if object.is_deleted:
            raise HTTPException(status_code=500, detail="User already deleted")

    @staticmethod
    async def convert_currencies(currency_from: str, currency_to: str, amount: float):
        match currency_from:
            case "USD":
                return amount / CurrencyEnum[currency_to].value
            case _:
                return amount * CurrencyEnum[currency_from].value
