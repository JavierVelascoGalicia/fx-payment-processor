
from typing import Optional, List

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
        )
    wallets: List["Wallet"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "noload"}
        )
    deleted_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=None))
    transactions: List["Transaction"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "noload"}
    )


class Wallet(SQLModel, table=True):
    __tablename__ = "wallets"

    wallet_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="users.user_id")
    balance: Optional[float] = Field(default=0.00)
    currency: str = Field(default="USD")
    created_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

    user: Optional[User] = Relationship(back_populates="wallets")
    transactions: List["Transaction"] = Relationship(back_populates="wallet", sa_relationship_kwargs={"lazy": "noload"})


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    wallet_id: int = Field(default=None, foreign_key="wallets.wallet_id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.user_id")
    currency: str = Field(default=None)
    amount: float = Field(default=None)
    transaction_type: int = Field(default=None)
    transaction_date: Optional[datetime] = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

    wallet: Optional[Wallet] = Relationship(back_populates="transactions", sa_relationship_kwargs={"lazy": "noload"})
    user: Optional[User] = Relationship(back_populates="transactions", sa_relationship_kwargs={"lazy": "noload"})
