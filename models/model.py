from sqlalchemy import Column, INTEGER, String , Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TodoList(Base):
    __tablename__ = "todolist"
    id = Column(INTEGER , primary_key = True)
    title = Column(String , nullable = False)
    complete = Column(Boolean, default = False)

class User(Base):
    __tablename__ = "todouser"
    email = Column(String, nullable=False, primary_key = True)
    password = Column(String,nullable = False)
    fullname = Column(String, nullable = False)