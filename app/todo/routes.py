import typing
from app.todo.views import AddTodo, AddUser, CompleteTodo, DeleteTodo, GetListTodo, ListUsers

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view('/add_todo', AddTodo)
    app.router.add_view('/list_todos', GetListTodo)
    app.router.add_view('/complete_todo', CompleteTodo)
    app.router.add_view('/add_user', AddUser)
    app.router.add_view('/list_users', ListUsers)
    app.router.add_view('/delete_todo', DeleteTodo)