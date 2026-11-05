
from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.user_model import User
from app.schemas.api_response import ApiResponse
from app.schemas.user_schemas import UserRequestDto, UserResponseDto, UserUpdateDto

user_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#used to hash passwords before saving them in the database
password_hasher = PasswordHasher()

#raise 409 if the username or email is already used by another user
def check_user_unique(db: Session, username: str = None, email: str = None, exclude_id: int = None):
    if username:
        query = db.query(User).filter(User.username == username)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        if query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    if email:
        query = db.query(User).filter(User.email == email)
        if exclude_id:
            query = query.filter(User.id != exclude_id)
        if query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

#create a new user
@user_router.post("/",response_model=ApiResponse,status_code=status.HTTP_201_CREATED)
def create_user(user_request_dto: UserRequestDto, db: Session = Depends(get_db)):
    check_user_unique(db, username=user_request_dto.username, email=user_request_dto.email)
    new_user = User(
        username=user_request_dto.username,
        email=user_request_dto.email,
        password=password_hasher.hash(user_request_dto.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return ApiResponse(status="success", message="User created successfully", data={"user": UserResponseDto.model_validate(new_user)})

#get all users
@user_router.get("/",response_model=ApiResponse)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return ApiResponse(status="success", message="Users retrieved successfully", data={"users": [UserResponseDto.model_validate(user) for user in users]})

#get user by id
@user_router.get("/{user_id}",response_model=ApiResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return ApiResponse(status="success", message="User retrieved successfully", data={"user": UserResponseDto.model_validate(user)})

# update user by id, only the fields sent in the request are updated
@user_router.put("/{user_id}",response_model=ApiResponse)
def update_user(user_id: int, user_update_dto: UserUpdateDto, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    check_user_unique(db, username=user_update_dto.username, email=user_update_dto.email, exclude_id=user_id)
    if user_update_dto.username is not None:
        user.username = user_update_dto.username
    if user_update_dto.email is not None:
        user.email = user_update_dto.email
    if user_update_dto.password is not None:
        user.password = password_hasher.hash(user_update_dto.password)
    db.commit()
    db.refresh(user)
    return ApiResponse(status="success", message="User updated successfully", data={"user": UserResponseDto.model_validate(user)})

# delete user by id
@user_router.delete("/{user_id}",response_model=ApiResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return ApiResponse(status="success", message="User deleted successfully", data={"user": UserResponseDto.model_validate(user)})
