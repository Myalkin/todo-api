from functools import wraps
from aiohttp.web import json_response
from marshmallow import ValidationError

def request_schema(schema_class):
    def decorator(handler):
        @wraps(handler)
        async def wrapper(view, *args, **kwargs):
            try:
                json_data = await view.request.json()
                schema = schema_class()
                validated_data = schema.load(json_data)

                view.request["data"] = validated_data

            except ValidationError as err:
                return json_response(
                    {"errors": err.messages},
                    status=400
                )

            return await handler(view, *args, **kwargs)

        return wrapper
    return decorator