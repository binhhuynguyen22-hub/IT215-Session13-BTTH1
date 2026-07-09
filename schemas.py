from pydantic import BaseModel, Field
from typing import Optional, Any

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str

class CreateMenu(BaseModel):
    dish_code: str
    dish_name:str
    calorie_count: int
    price: float
class UpdateMenu(BaseModel):
    dish_code: str
    dish_name:str
    calorie_count: int
    price: float
    status: str