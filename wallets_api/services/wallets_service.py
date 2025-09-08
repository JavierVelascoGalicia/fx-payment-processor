
from sqlmodel import Session, select

from fastapi import HTTPException

from typing import Sequence
from wallets_api.models.models import Wallet
from wallets_api.schemas.transactions import TransactionRequest, ConvertTransactionRequest
from wallets_api.utils.utils import Utils
from wallets_api.utils.enums import TransactionTypeEnum
from wallets_api.services.transactions_service import TransactionService
from wallets_api.services.users_service import UserService


class WalletService:

    @staticmethod
    async def create_wallet(user_id: str, currency: str, session: Session) -> Wallet:
        wallet = Wallet(user_id=user_id, currency=currency)
        session.add(wallet)
        session.commit()
        session.refresh(wallet)
        return wallet

    @staticmethod
    async def get_wallet_by_user_id_and_currency(user_id: str, currency: str, session: Session):
        # Get the user and validate if is not deleted
        await UserService.get_user_by_id(user_id, session)
        # Retrieve the wallet
        wallet = session.exec(select(Wallet).where(Wallet.user_id == user_id, Wallet.currency == currency)).one_or_none()
        if not wallet:
            wallet = await WalletService.create_wallet(user_id, currency, session)
        return wallet

    @staticmethod
    async def get_wallets_by_user_id(user_id: str, session: Session) -> Sequence[Wallet]:
        # Get the user and validate if is not deleted
        await UserService.get_user_by_id(user_id, session)
        return session.exec(select(Wallet).where(Wallet.user_id == user_id)).all()

    @staticmethod
    async def get_balance(user_id: str, session: Session) -> dict:
        wallets = await WalletService.get_wallets_by_user_id(user_id, session)

        await Utils.validate_response(wallets)

        balance = {}
        for wallet in wallets:
            balance[wallet.currency] = wallet.balance

        return balance

    @staticmethod
    async def fund_withdraw_wallet(user_id: str, body: TransactionRequest, transaction_type: TransactionTypeEnum, session: Session) -> TransactionRequest:
        wallet = await WalletService.get_wallet_by_user_id_and_currency(user_id, body.currency, session)
        match transaction_type.name:
            case 'FUND':
                wallet.balance += body.amount
            case 'WITHDRAW':
                if wallet.balance < body.amount:
                    raise HTTPException(status_code=500, detail="No funds")
                wallet.balance -= body.amount

        await TransactionService.create_transaction(user_id, body, transaction_type, wallet.wallet_id, session)

        session.add(wallet)
        session.commit()
        session.refresh(wallet)

        return TransactionRequest(amount=wallet.balance, currency=wallet.currency)

    @staticmethod
    async def convert_balance(user_id: str, body: ConvertTransactionRequest, session: Session) -> dict:
        await WalletService.fund_withdraw_wallet(user_id, TransactionRequest(currency=body.from_currency, amount=body.amount), TransactionTypeEnum.WITHDRAW, session)
        converted_amount = await Utils.convert_currencies(currency_from=body.from_currency, currency_to=body.to_currency, amount=body.amount)
        await WalletService.fund_withdraw_wallet(user_id, TransactionRequest(currency=body.to_currency, amount=converted_amount), TransactionTypeEnum.FUND, session)

        return await WalletService.get_balance(user_id, session)
