from fastapi import APIRouter, status
from fastapi_pagination import Page, paginate
from db.db2 import SessionDep
from models import Transaction, TransactionCreate
from services.transaction_service import (
    create_transaction,
    list_transactions,
    delete_transaction,
    get_transaction_or_404,
)

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=Transaction
)
async def create_transaction_endpoint(
    transaction_data: TransactionCreate,
    session: SessionDep,
):
    return create_transaction(session, transaction_data)


@router.get("/", response_model=Page[Transaction])
async def list_transactions_endpoint(
    session: SessionDep,
    customer_id: int | None = None,
    min_amount: int | None = None,
    max_amount: int | None = None,
):
    transactions = list_transactions(
        session=session,
        customer_id=customer_id,
        min_amount=min_amount,
        max_amount=max_amount,
    )
    return paginate(transactions)


@router.get("/{transaction_id}", response_model=Transaction)
async def get_transaction_endpoint(
    transaction_id: int,
    session: SessionDep,
):
    return get_transaction_or_404(session, transaction_id)


@router.delete(
    "/{transaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_transaction_endpoint(
    transaction_id: int,
    session: SessionDep,
):
    delete_transaction(session, transaction_id)
    return None
