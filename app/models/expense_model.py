from app.core.db import Base, engine
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime,Boolean

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String(50), nullable=False, index=True)
    description = Column(String(200), index=True,nullable=True)
    show = Column(Boolean, default=True)
    amount = Column(Float,nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)    
