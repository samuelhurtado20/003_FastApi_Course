from typing import Optional, List
from sqlmodel import Session, select
from fastapi import HTTPException, status
from models import Transaction, TransactionCreate, Customer


def create_transaction(
    session: Session, data: TransactionCreate
) -> Transaction:
    # validar que el customer exista
    customer = session.get(Customer, data.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer doesn't exist",
        )

    transaction = Transaction(**data.model_dump())
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def list_transactions(
    session: Session,
    customer_id: Optional[int] = None,
    min_amount: Optional[int] = None,
    max_amount: Optional[int] = None,
) -> list[Transaction]:
    query = select(Transaction)

    if customer_id is not None:
        query = query.where(Transaction.customer_id == customer_id)
    if min_amount is not None:
        query = query.where(Transaction.ammount >= min_amount)
    if max_amount is not None:
        query = query.where(Transaction.ammount <= max_amount)

    return session.exec(query).all()


def get_transaction_or_404(session: Session, transaction_id: int) -> Transaction:
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return transaction


def delete_transaction(session: Session, transaction_id: int) -> None:
    transaction = get_transaction_or_404(session, transaction_id)
    session.delete(transaction)
    session.commit()
    return