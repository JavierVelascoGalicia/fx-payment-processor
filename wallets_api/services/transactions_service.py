
from sqlmodel import Session, select
from wallets_api.utils.enums import TransactionTypeEnum
from wallets_api.models.models import Transaction
from wallets_api.schemas.transactions import TransactionRequest


class TransactionService:

    @staticmethod
    async def create_transaction(user_id: str, transactionRequest: TransactionRequest, transaction_type: TransactionTypeEnum, wallet_id: str, session: Session):
        transaction = Transaction(user_id=user_id, transaction_type=transaction_type.value, wallet_id=wallet_id, amount=transactionRequest.amount, currency=transactionRequest.currency)
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction

    @staticmethod
    async def get_all_transactions_by_user_id(user_id, session: Session):
        return session.exec(select(Transaction).where(Transaction.user_id == user_id)).all()

    @staticmethod
    async def get_all_transactions_by_wallet_id(wallet_id: str, session: Session):
        return session.exec(select(Transaction).where(Transaction.wallet_id == wallet_id)).all()
