from pydantic import BaseModel

class Chit(BaseModel):
    id: int | None = None
    chit_name: str
    amount: float
    duration_months: int
    total_members: int
    status: str = "active"