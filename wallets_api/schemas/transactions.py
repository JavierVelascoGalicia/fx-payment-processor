

from pydantic import BaseModel


class TransactionRequest(BaseModel):
    currency: str
    amount: float


class ConvertTransactionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
