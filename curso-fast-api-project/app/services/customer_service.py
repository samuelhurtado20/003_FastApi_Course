from typing import Optional, List
from sqlmodel import Session, select
from fastapi import HTTPException, status
from models import Customer, CustomerCreate, CustomerUpdate


def get_customer_or_404(session: Session, customer_id: int) -> Customer:
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer


def list_customers(
    session: Session,
    name: Optional[str] = None,
    email: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
) -> list[Customer]:
    query = select(Customer)

    if name:
        query = query.where(Customer.name.ilike(f"%{name}%"))
    if email:
        query = query.where(Customer.email == email)
    if min_age is not None:
        query = query.where(Customer.age >= min_age)
    if max_age is not None:
        query = query.where(Customer.age <= max_age)

    return session.exec(query).all()


def create_customer(session: Session, data: CustomerCreate) -> Customer:
    # si quieres validar unicidad de email aquí:
    if data.email:
        existing = session.exec(
            select(Customer).where(Customer.email == data.email)
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    customer = Customer(**data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def update_customer_put(
    session: Session, customer_id: int, data: CustomerUpdate
) -> Customer:
    customer = get_customer_or_404(session, customer_id)

    update_data = data.model_dump()
    customer.sqlmodel_update(update_data)

    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def update_customer_patch(
    session: Session, customer_id: int, data: CustomerUpdate
) -> Customer:
    customer = get_customer_or_404(session, customer_id)

    update_data = data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(update_data)

    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def delete_customer(session: Session, customer_id: int) -> None:
    customer = get_customer_or_404(session, customer_id)
    session.delete(customer)
    session.commit()
    return