from pydantic import BaseModel


class CreateWalletRequest(BaseModel):
    currency: str
