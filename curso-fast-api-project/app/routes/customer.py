from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from app.db.db2 import SessionDep       
from app.models.customer import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()

# ============================================================
# GET /customers/{id}
# ============================================================
@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# ============================================================
# PUT /customers/{id}  (REEMPLAZA COMPLETO)
# ============================================================
@router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer_put(customer_id: int, data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Reemplaza todo (PUT)
    update_data = data.model_dump()

    customer_db.sqlmodel_update(update_data)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)

    return customer_db


# ============================================================
# PATCH /customers/{id}  (ACTUALIZA SOLO CAMPOS ENVIADOS)
# ============================================================
@router.patch("/customers/{customer_id}", response_model=Customer)
async def update_customer_patch(customer_id: int, data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)

    if not customer_db:
        raise HTTPException(status_code=404, detail="Customer not found")

    update_data = data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(update_data)

    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)

    return customer_db
