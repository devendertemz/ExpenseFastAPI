from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DATABASE_URL = "sqlite:///./expense.db"

#create engine
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

#session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#dependency
#this function will be used to get a database session for each request
def get_db():
    db = SessionLocal()
    #return the database session to the caller and close it after the request is done
    try:
        # this is a generator function, it will yield the database session to the caller and then close it after the request is done
        yield db
    finally:
        # it always execute and the close should be called to close the database session after the request is done
        db.close()
        
Base = declarative_base()