class CustomerPlan(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)    
    customer_id: int = Field(foreign_key="customer.id")
    plan_id:int = Field(foreign_key="plan.id")
    status:Optional[bool] = Field(default=True)


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELED = "canceled"

class CustomerPlan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    plan_id: int = Field(foreign_key="plan.id")
    customer_id: int = Field(foreign_key="customer.id")
    status: SubscriptionStatus = Field(default=SubscriptionStatus.ACTIVE)
