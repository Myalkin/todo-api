import uuid
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__="users"
    id = Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4, nullable= False)
    name = Column(String(150), unique= True, nullable= False)
    password_hash = Column(String(255), nullable=False) 

class Todo(Base):
    __tablename__="todos"
    id = Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4, nullable= False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable= False)
    task = Column(String(255), nullable= False)
    is_complete = Column(Boolean, nullable=False)

# @dataclass
# class Todo:
#     _id: uuid.UUID
#     user_id: uuid.UUID
#     task: str
#     is_comlpete: bool

# @dataclass
# class User:
#     _id: uuid.UUID
#     name: str
#     password: str