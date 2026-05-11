import typing

from app.store.todo.accessor import TodoAccessor

if typing.TYPE_CHECKING:
    from app.web.app import Application

def setup_accessors(app:"Application"):
    app.todo_accessor = TodoAccessor()
    app.on_startup.append(app.todo_accessor.connect)
    app.on_cleanup.append(app.todo_accessor.disconnect)