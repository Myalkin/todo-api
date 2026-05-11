from marshmallow import Schema, fields

class OkRersponseSchema(Schema):
    status: fields.Str(required=True)
    data: fields.Dict