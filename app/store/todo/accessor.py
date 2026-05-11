from typing import Optional
import typing

from sqlalchemy import select

from app.todo.models import Todo, User
if typing.TYPE_CHECKING:
    from app.web.app import Application


class TodoAccessor:
    def __init__(self):
        self.app: Optional[Application]= None
    
    async def connect(self, app: "Application"):
        self.app = app
        try:
            self.app.database["todos"]
        except KeyError:
            self.app.database["todos"] = []
        print("Connect to DataBase")


    async def disconnect(self, _: "Application"):
        self.app = None
        print("Disconnect from DataBase")

    async def add_user(self, session, user: User):
        session.add(user)
        await session.commit()
    
    async def list_users(self, session)->list[User]:
        result = await session.execute(select(User))
        return result.scalars().all()
    
    async def user_exists(self,session, _id:str)-> bool:
        if await session.execute(select(User).where(id=str(_id))):
            return True
        return False


    async def add_todo(self,session, todo: Todo):
        session.add(todo)
        await session.commit()

    async def list_todos(self, session) -> list[Todo]:
        result = await session.execute(select(Todo))
        return result.scalars().all()
    
    async def complete_todo(self, session, todo_id)->bool:
        result = await session.execute(select(Todo).where(Todo.id == str(todo_id)))
        todo = result.scalars().first()
        if not todo:
            return False
        else:
            todo.is_complete = not todo.is_complete
            await session.commit()
            return True
    
    async def delete_todo(self, session, todo_id:str)-> bool:
        result = await session.execute(select(Todo).where(Todo.id == todo_id))
        todo = result.scalars().first()
        if not todo:
            return False
        await session.delete(todo)
        await session.commit()
        return True
        

