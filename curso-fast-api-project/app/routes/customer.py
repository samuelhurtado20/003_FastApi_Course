from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from db.db2 import SessionDep
from models.customer import Customer, CustomerCreate, CustomerUpdate


router = APIRouter()


@router.get('/customers/{customer_id}', response_model=Customer)
async def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get('/customer/{customer_id}', response_model=Customer)
async def read_customer(customer_id:int, session: SessionDep):
  cst = select(Customer).where(Customer.id == customer_id)
  customer_db = session.exec(cst).first()
  if not customer_db:
        raise HTTPException(
            status_code=404, detail="Customer not found"
    )

  return customer_db


@router.put("/update_customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_data: CustomerCreate, session: SessionDep) -> Customer:
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente con ID {customer_id} no encontrado")
    customer_db.name = customer_data.name
    customer_db.description = customer_data.description
    customer_db.email = customer_data.email
    customer_db.age = customer_data.age
    session.add(customer_db) # Agregar el cliente actualizado a la sesión
    session.commit() # Guardar los cambios en la base de datos
    session.refresh(customer_db) # Refrescar el objeto cliente para obtener los datos actualizados
    return customer_db


@router.patch("/customers/{id}", response_model=Customer, status_code=status.HTTP_201_CREATED,)
async def update_customer(id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    old_data = customer_data
    update_data = customer_data.model_dump(exclude_unset=True)
    #Revisando cambios de los datos
    if old_data.name != update_data['name']:
        update_data['name'] = old_data.name
    if old_data.description != update_data['description']:
        update_data['description'] = old_data.description
    if old_data.email != update_data['email']:
        update_data['email'] = old_data.email    
    if old_data.age != update_data['age']:
        update_data['age'] = old_data.age

    customer.sqlmodel_update(update_data)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.patch("/customer/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def read_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer doesn't exist"
        )
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db
