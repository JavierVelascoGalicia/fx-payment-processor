from pydantic import BaseModel
from datetime import datetime


class CreateWalletRequest(BaseModel):
    currency: str


class CreateWalletResponse(CreateWalletRequest):
    user_id: int
    balance: float
    created_at: datetime
    updated_at: datetime
