

from pydantic import BaseModel


class Transaction(BaseModel):
    currency: str
    amount: float


class ConvertTransactionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
