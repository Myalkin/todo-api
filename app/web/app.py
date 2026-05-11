from typing import Optional

from aiohttp.web import Application as AiohttpApplication
from app.db import AsyncSessionLocal
from app.store.todo.accessor import TodoAccessor
from app.web.routes import setup_routes


class Application(AiohttpApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_session = AsyncSessionLocal

def create_app():
    app = Application()
    app.database = {"users":[], "todos":[]}
    app.todo_accessor = TodoAccessor()
    import asyncio
    asyncio.run(app.todo_accessor.connect(app)) 
    setup_routes(app)
    return app


app = create_app()