from sqlalchemy import Column, Integer, String, Table, MetaData, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from api._module import TodoItem
# from api.database import Base

metadata = MetaData()
class Base(DeclarativeBase):
    pass

class Todolist(Base) :
    __tablename__ = 'todolist'    
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title : Mapped[str] = mapped_column(String(100))
    completed : Mapped[bool] = mapped_column(default=False)