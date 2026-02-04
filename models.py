from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    role: str


class Order(BaseModel):
    order_id: Optional[int] = None
    user_id: int
    product: str
    quantity: int
    status: str = "CREATED"
