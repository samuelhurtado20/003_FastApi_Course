from fastapi import APIRouter
from models import Plan
from db import session

router = APIRouter()

@router.post('/plans')
def create_plan(plan_data: Plan):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db


@router.post('/customers/{customer_id}/plans/{plan_id}')
async def subscribe_customer_to_plan(customer_id: int, plan_id: int):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)

    if not customer_db or not plan_db:
        raise HTTPException(status_code=404, detail="El customer o plan no existe")

    customer_plan_db = CustomerPlan(plan_id=plan_db.id, customer_id=customer_db.id)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_db)

    return customer_plan_db

@router.get('/customers/{customer_id}/plans')
def list_customer_plans(customer_id: int):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=404, detail="El customer no existe")
    return customer_db.plans



# check schema 
# sqlite3 nombre_base.db
# .schema nombre_tabla
