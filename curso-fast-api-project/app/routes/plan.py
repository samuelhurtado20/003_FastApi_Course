from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from app.models.plan import Plan
from app.db.db2 import SessionDep
from app.models.customer import Customer
from app.models.plan import CustomerPlan, SubscriptionStatus


router = APIRouter()

@router.post('/plans')
def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.post('/customers/{customer_id}/plans/{plan_id}')
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(status_code=404, detail="El customer o plan no existe")

    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_db)

    return customer_plan_db


@router.post('/customers/{customer_id}/subscribe/{plan_id}')
async def subscribe_customer_to_plan(customer_id, plan_id: int, session: SessionDep, status: SubscriptionStatus = Query(default=SubscriptionStatus.ACTIVE)):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    
    if not customer_db or not plan_db:
        raise HTTPException(status_code=404, detail="Customer or Plan not found")

    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id, status=status)

    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get('/customers/{customer_id}/plans/active', response_model=list[Plan])
async def list_active_plans(customer_id: int, session: SessionDep):
    stmt = (
        select(Plan)
        .join(CustomerPlan, CustomerPlan.plan_id == Plan.id)
        .where(
            CustomerPlan.customer_id == customer_id,
            CustomerPlan.status == SubscriptionStatus.ACTIVE
        )
    )
    return session.exec(stmt).all()


@router.get('/customers/{customer_id}/plans', response_model=list[Plan])
async def list_customer_plans(
    customer_id: int,
    session: SessionDep,
    status: Optional[SubscriptionStatus] = Query(default=None)
):
    if status is None:
        # all plans by customer
        customer_db = session.get(Customer, customer_id)
        if not customer_db:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer_db.plans

    # plans by customer and filtered by status
    stmt = (
        select(Plan)
        .join(CustomerPlan, CustomerPlan.plan_id == Plan.id)
        .where(
            CustomerPlan.customer_id == customer_id,
            CustomerPlan.status == status
        )
    )
    return session.exec(stmt).all()
# check schema 
# sqlite3 nombre_base.db
# .schema nombre_tabla
