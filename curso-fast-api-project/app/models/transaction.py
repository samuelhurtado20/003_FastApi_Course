from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .customer import Customer


class TransactionBase(SQLModel):
    ammount: int
    description: str


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    customer: "Customer" = Relationship(sa_relationship=True, back_populates="transactions")


class TransactionCreate(TransactionBase):
    customer_id: int
