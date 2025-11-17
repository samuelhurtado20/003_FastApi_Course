from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .transaction import Transaction


class CustomerBase(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    email: EmailStr
    age: Optional[int] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None


class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(sa_relationship=True, back_populates="customer")
