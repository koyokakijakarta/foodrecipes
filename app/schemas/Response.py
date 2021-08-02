from app import ma


class ResponseSchema(ma.Schema):
    success = ma.Bool()
    message = ma.Str()
    errors = ma.Dict()
    token = ma.Str()
