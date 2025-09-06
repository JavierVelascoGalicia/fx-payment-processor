
from sqlmodel import Session, select

from fastapi import HTTPException

from typing import Sequence
from wallets_api.models.models import Wallet
from wallets_api.schemas.transactions import Transaction, ConvertTransactionRequest
from wallets_api.utils.utils import Utils
from wallets_api.utils.enums import TransactionTypeEnum
from wallets_api.schemas.wallet import CreateWalletRequest, CreateWalletResponse


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
        wallet = session.exec(select(Wallet).where(Wallet.user_id == user_id, Wallet.currency == currency)).one_or_none()
        if not wallet:
            wallet = await WalletService.create_wallet(user_id, currency, session)
        return wallet

    @staticmethod
    async def get_wallets_by_user_id(user_id: str, session: Session) -> Sequence[Wallet]:
        return session.exec(select(Wallet).where(Wallet.user_id == user_id)).all()

    @staticmethod
    async def get_balance(user_id: str, session: Session) -> dict:
        wallets = await WalletService.get_wallets_by_user_id(user_id, session)
        balance = {}
        for wallet in wallets:
            balance[wallet.currency] = wallet.balance

        return balance

    @staticmethod
    async def fund_withdraw_wallet(user_id: str, body: Transaction, transaction_type: TransactionTypeEnum, session: Session) -> Transaction:
        wallet = await WalletService.get_wallet_by_user_id_and_currency(user_id, body.currency, session)
        match transaction_type.name:
            case 'FUND':
                wallet.balance += body.amount
            case 'WITHDRAW':
                if wallet.balance < body.amount:
                    raise HTTPException(status_code=500, detail="No founds")
                wallet.balance -= body.amount

        session.add(wallet)
        session.commit()
        session.refresh(wallet)

        return Transaction(amount=wallet.balance, currency=wallet.currency)
    
    @staticmethod
    async def convert_balance(user_id: str, body: ConvertTransactionRequest, session: Session) -> dict:
        await WalletService.fund_withdraw_wallet(user_id, Transaction(currency=body.from_currency, amount=body.amount), TransactionTypeEnum.WITHDRAW, session)
        converted_amount = await Utils.convert_currencies(currency_from=body.from_currency, currency_to=body.to_currency, amount=body.amount)
        await WalletService.fund_withdraw_wallet(user_id, Transaction(currency=body.to_currency, amount=converted_amount), TransactionTypeEnum.FUND, session)
        
        return await WalletService.get_balance(user_id, session)
