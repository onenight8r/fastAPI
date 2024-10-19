from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DTABASE_URL='postgresql://postgres:123qwe@localhost/fastapi'
engine = create_engine(SQLALCHEMY_DTABASE_URL)

SessionLocal = sessionmaker(autoflush=False,bind=engine)

Base=declarative_base()

#DEPENDENCY 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
