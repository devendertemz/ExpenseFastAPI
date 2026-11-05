from fastapi import FastAPI
import app.models.user_model
import app.models.expense_model
from app.core.db import Base, engine
from app.routers.expense_route import expense_router
from app.routers.user_route import user_router
from app.routers.auth import auth_router

#create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(expense_router)
app.include_router(auth_router)
@app.get("/")
def root():
    return {"Hello": "World"}
