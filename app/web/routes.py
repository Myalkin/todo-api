import typing
from app.todo.routes import setup_routes as todo_setup_routes

if typing.TYPE_CHECKING:
    from app.web.app import Application

def setup_routes(app: "Application"):
    todo_setup_routes(app)