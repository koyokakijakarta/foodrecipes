from app import ma
from app.models import Recipe as RecipeModels
from app.schemas.Response import ResponseSchema
from marshmallow import validate, ValidationError, EXCLUDE, post_load


def validate_image(image):
    allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
    if "." not in image or ("." in image and image.rsplit(".", 1)[1].lower() not in allowed_extensions):
        raise ValidationError("Image type must be a png, jpg, jpeg, or gif")


class RecipeSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
    id = ma.Int()
    user = ma.Str()
    name = ma.Str(required=True, validate=validate.Length(min=1))
    country = ma.Str(required=True, validate=validate.Length(min=1))
    category = ma.Str(required=True, validate=validate.Length(min=1))
    image = ma.Str(required=True, validate=validate_image)


class RecipeSchema2(RecipeSchema):
    description = ma.Str(required=True)


class Recipe(RecipeSchema2):
    id_user = ma.Int(required=True)

    @post_load
    def create_recipe(self, data, **_):
        return RecipeModels.Recipe(**data)


class RecipeAll(ResponseSchema):
    data = ma.Nested(RecipeSchema, many=True)


class RecipeDetail(ResponseSchema):
    data = ma.Nested(RecipeSchema2)
