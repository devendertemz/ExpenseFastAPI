from datetime import datetime

from pydantic import BaseModel,Field

class ExpenseRequestDto(BaseModel):
    title: str = Field(..., description="Expense title",min_length=2, max_length=100)
    amount: float = Field(..., description="Expense amount", gt=0)
    description: str = Field(..., description="Expense description",     max_length=200)
    show: bool=Field( description="Show expense or not", default=True)

class ExpenseResponseDto(BaseModel):
    id: int = Field(..., description="Expense ID")
    title: str = Field(..., description="Expense title")
    amount: float = Field(..., description="Expense amount")
    description: str = Field(..., description="Expense description")
    show: bool = Field(..., description="Show expense or not")
    created_at: datetime = Field(description="Expense creation date")

    model_config = {
        "from_attributes": True,
   }

