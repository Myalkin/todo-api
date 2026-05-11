from marshmallow import Schema,fields,validate

from app.web.schemes import OkRersponseSchema

class UserAddSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(required=True, validate=validate.Length(min=8))

class UserSchema(Schema):
    id = fields.UUID(required=True, attribute='_id')

class ListUserShema(Schema):
    users = fields.Nested(UserSchema, many=True)

class ListUsersResponceSchema(OkRersponseSchema):
    data = fields.Nested(ListUserShema)

class TodoAddSchema(Schema):
    user_id = fields.UUID(required=True, attribute='_id')
    task = fields.Str(required=True, validate=validate.Length(min=3))

class TodoSchema(Schema):
    id = fields.UUID(required=True, attribute='_id')

class TodoRequiredSchema(Schema):
    id = fields.UUID(required=True)

class ListTodoSchema(Schema):
    todos = fields.Nested(TodoSchema, many=True)

class ListTodoResponseSchema(OkRersponseSchema):
    data = fields.Nested(ListTodoSchema)