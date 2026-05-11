import uuid
from aiohttp.web_response import json_response
from aiohttp_apispec import response_schema
import bcrypt
from app.web.decorators import request_schema
from app.todo.models import Todo, User
from app.todo.schemes import ListTodoResponseSchema, ListUsersResponceSchema, TodoAddSchema, TodoRequiredSchema, TodoSchema, UserAddSchema
from app.web.base import View
from app.web.schemes import OkRersponseSchema

class AddUser(View):
    @request_schema(UserAddSchema)
    @response_schema(OkRersponseSchema, 200)
    async def post(self):
        data = self.request['data']
        user = User(id = uuid.uuid4(), name=data['name'], password_hash=str(bcrypt.hashpw(data['password'].encode('UTF-8'), salt=bcrypt.gensalt()).decode()))
        async with self.request.app.db_session() as session:
            async with session.begin():
                await self.request.app.todo_accessor.add_user(session, user)
        return json_response(data={'status': 'ok'})

class ListUsers(View):
    @response_schema(ListUsersResponceSchema, 200)
    async def get(self):
        async with self.request.app.db_session() as session:
            users = await self.request.app.todo_accessor.list_users(session)
        raw_users = [{
                "id": str(user.id),
                "name": user.name,
            } 
            for user in users
        ]
        return json_response(data={"users":raw_users})

class AddTodo(View):
    @request_schema(TodoAddSchema)
    @response_schema(OkRersponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        user_id = data.get("user_id")
        async with self.request.app.db_session() as session:
            if self.request.app.todo_accessor.user_exists(session, user_id):
                todo = Todo(id = uuid.uuid4(), user_id=data['user_id'], task=data['task'],  is_complete = False)
            else:
                return json_response(data={'error':'user not found'})
            await self.request.app.todo_accessor.add_todo(session, todo)
        return json_response(data={'status': 'ok'})

class GetListTodo(View):
    @response_schema(ListTodoResponseSchema, 200)
    async def get(self):
        async with self.request.app.db_session() as session:
            todos = await self.request.app.todo_accessor.list_todos(session)  
        raw_todos = [
            {
                "id": str(todo.id),
                "user":str(todo.user_id),
                "task": todo.task,
                "done": todo.is_complete
            } 
            for todo in todos
        ]
        
        return json_response(data={"todos": raw_todos})
    
class CompleteTodo(View):
    @request_schema(TodoRequiredSchema)
    @response_schema(OkRersponseSchema, 200)
    async def patch(self):
        data = self.request['data']
        todo_id = str(data.get("id"))
        async with self.request.app.db_session() as session:
            if not todo_id:
                return json_response({"error": "id is required"}, status=400)
            updated = await self.request.app.todo_accessor.complete_todo(session, todo_id)
            if updated:
                return json_response({"status": "updated"})
            else:
                return json_response({"error": "todo not found"}, status=404)
        
class DeleteTodo(View):
    @request_schema(TodoRequiredSchema)
    async def delete(self):
        data = self.request['data']
        todo_id = str(data.get("id"))
        if not todo_id:
                return {"error": "id is required"}, 400
        async with self.request.app.db_session() as session:
            deleted = await self.request.app.todo_accessor.delete_todo(session, todo_id)
        if deleted:
            return json_response({"status": "deleted"})
        else:
            return json_response({"error": "todo not found"}, status=404)