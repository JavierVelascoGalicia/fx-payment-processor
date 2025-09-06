
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from wallets_api.database import get_db_session
from wallets_api.models.models import Wallet
from wallets_api.schemas.wallet import CreateWalletResponse, CreateWalletRequest
from wallets_api.schemas.transactions import Transaction, ConvertTransactionRequest
from wallets_api.services.wallets_service import WalletService
from wallets_api.utils.enums import TransactionTypeEnum

wallet_controller = APIRouter(prefix="/wallets", tags=["wallets"])


@wallet_controller.get("/{user_id}", response_model=List[Wallet])
async def get_wallets_by_user_id(user_id: str, session: Session = Depends(get_db_session)):
    return await WalletService.get_wallets_by_user_id(user_id, session)


@wallet_controller.post("/{user_id}", response_model=Wallet)
async def create_wallet(user_id: str, body: CreateWalletRequest, session: Session = Depends(get_db_session)):
    return await WalletService.get_wallet_by_user_id_and_currency(user_id, body.currency, session)


@wallet_controller.post("/{user_id}/fund", response_model=Transaction)
async def fund_wallet(user_id: str, body: Transaction, session: Session = Depends(get_db_session)) ->  Transaction:
    return await WalletService.fund_withdraw_wallet(user_id, body, TransactionTypeEnum.FUND, session)


@wallet_controller.post("/{user_id}/withdraw", response_model=Transaction)
async def withdraw(user_id: str, body: Transaction, session: Session = Depends(get_db_session)) ->  Transaction:
    return await WalletService.fund_withdraw_wallet(user_id, body, TransactionTypeEnum.WITHDRAW, session)    


@wallet_controller.get("/{user_id}/balances", response_model=dict)
async def get_balances(user_id: str, session: Session = Depends(get_db_session)) -> dict:
    response = await WalletService.get_balance(user_id, session)
    return response


@wallet_controller.post("/{user_id}/convert", response_model=dict)
async def convert_currencies(user_id: str, body: ConvertTransactionRequest, session: Session = Depends(get_db_session)) -> dict:
    return await WalletService.convert_balance(user_id, body, session)
