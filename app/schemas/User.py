from app import ma
from app.models import User as UserModels
from app.schemas.Response import ResponseSchema
from marshmallow import validate, validates, ValidationError, post_load


class UserSchema(ma.Schema):
    id = ma.Integer()
    fullname = ma.Str(required=True)
    username = ma.Str(required=True, validate=validate.Length(min=5, max=30))
    email = ma.Email(required=True)

    @validates("username")
    def validate_username(self, username):
        err = []
        s = False
        word_accept = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ."
        for i in range(len(username)):
            if username[i] not in [word_accept[n] for n in range(len(word_accept))]:
                s = True
        if s:
            err.append("Only letters (a-z), numbers (0-9), and periods (.) are allowed!")
        if username[0] == ".":
            err.append("The first character must be an ascii letter (a-z) or number (0-9)!")
        if username[-1] == ".":
            err.append("The last character must be an ascii letter (a-z) or number (0-9)!")
        if err:
            raise ValidationError(err)


class UserSchema2(UserSchema):
    role = ma.Str(validate=validate.OneOf(["admin", "user"]))
    created_at = ma.DateTime()
    updated_at = ma.DateTime()


class User(UserSchema2):
    token = ma.Str(required=True)
    password = ma.Str(required=True)
    salt = ma.Str(required=True)

    @post_load
    def create_user(self, data, **_):
        return UserModels.User(**data)


class UserAll(ResponseSchema):
    data = ma.Nested(UserSchema, many=True)


class UserDetail(ResponseSchema):
    data = ma.Nested(UserSchema2)
