from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
class Post(Base): #it will create the table if not already prestn
    __tablename__="posts"

    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published= Column(Boolean,server_default='True',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))


