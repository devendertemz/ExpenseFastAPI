from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.jwt_helper import create_access_token
from app.models.user_model import User
from app.schemas.user_schemas import LoginRequestDto, LoginResponseDto, UserResponseDto

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth_router.post("/",response_model=LoginResponseDto)
def login_user(login_req:LoginRequestDto, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == login_req.email).first()
    if not db_user or not db_user.verify_password(login_req.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": db_user.email})
    return LoginResponseDto(access_token=access_token, user=UserResponseDto.model_validate(db_user))