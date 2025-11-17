from enum import Enum
from typing import TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel
if TYPE_CHECKING:
    from .customer import Customer

class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELED = "canceled"

class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: SubscriptionStatus = Field(default=SubscriptionStatus.ACTIVE)


class PlanBase(SQLModel):
    name: str = Field(default=None)
    price: int = Field(default=None)
    descripcion: str = Field(default=None)


class Plan(PlanBase, table=True):
    id: int | None = Field(primary_key=True)
    # customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan)



# class CustomerPlan(SQLModel, table=True):
#     id: Optional[int] = Field(primary_key=True, default=None)    
#     customer_id: int = Field(foreign_key="customer.id")
#     plan_id:int = Field(foreign_key="plan.id")
#     status:Optional[bool] = Field(default=True)