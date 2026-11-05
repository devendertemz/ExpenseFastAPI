from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserRequestDto(BaseModel):
    username: str = Field(..., description="Username", min_length=3, max_length=50)
    email: EmailStr = Field(..., description="User email", max_length=100)
    password: str = Field(..., description="User password", min_length=6, max_length=100)

# all fields optional, only the ones sent will be updated
class UserUpdateDto(BaseModel):
    username: Optional[str] = Field(None, description="Username", min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None, description="User email", max_length=100)
    password: Optional[str] = Field(None, description="User password", min_length=6, max_length=100)

# password is never returned in the response
class UserResponseDto(BaseModel):
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="User email")
    created_at: datetime = Field(description="User creation date")

    model_config = {
        "from_attributes": True,
    }


class LoginRequestDto(BaseModel):
    email: EmailStr = Field(..., description="User email", max_length=100)
    password: str = Field(..., description="User password", min_length=2, max_length=100)


class LoginResponseDto(BaseModel):
    access_token:str
    user: UserResponseDto