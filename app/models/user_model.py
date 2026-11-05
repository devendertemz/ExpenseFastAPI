from app.core.db import Base, engine
from datetime import datetime
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError
from sqlalchemy import Column, Integer, String, Float, DateTime,Boolean

_password_hasher = PasswordHasher()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    email = Column(String(100), index=True,nullable=False,unique=True,)
    password = Column(String(200),nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # check a plain-text password against the stored argon2 hash
    def verify_password(self, plain_password: str) -> bool:
        try:
            return _password_hasher.verify(self.password, plain_password)
        except (VerificationError, InvalidHashError):
            # wrong password, or the stored value isn't a valid argon2 hash
            return False