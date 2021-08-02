from app import app, request, db
from app.models import Recipe as RecipeModels
from app.models.User import User
from app.schemas.Recipe import Recipe, RecipeAll, RecipeDetail
from app.schemas.Response import ResponseSchema
from app.services.CloudinaryUpload import upload as upload_cloudinary
from app.services.ImgBBUpload import upload as upload_imgbb
from app.services.LocalUpload import upload as upload_local
from werkzeug.utils import secure_filename
from marshmallow import ValidationError


class Recipe:
    RESPONSE = ResponseSchema()
    recipes_schema = RecipeAll()
    recipe_schema = RecipeDetail()
    Recipe = Recipe()

    def all(self):
        data = RecipeModels.Recipe.query.filter_by(deleted_at=None).order_by(RecipeModels.Recipe.id)
        user = None
        if request.args.get("user"):
            user = User.query.filter_by(username=request.args.get("user")).first()
            if user:
                data = data.filter_by(id_user=user.id)
        if request.args.get("name"):
            data = data.filter(RecipeModels.Recipe.name.like(f"%{request.args.get('name')}%"))
        if request.args.get("country"):
            data = data.filter(RecipeModels.Recipe.country.like(f'%{request.args.get("country")}%'))
        data = data.all() if not user else []
        return self.recipes_schema.dump({
            "success": True,
            "message": "success retrieve data",
            "data": data
        })

    def add(self, user):
        data = request.form
        try:
            recipe = data.copy()
            recipe["id_user"] = user.id
            if "image" in recipe and "image" not in request.files:
                del recipe["image"]
            if "image" in request.files:
                allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
                image = request.files["image"]
                filename = secure_filename(image.filename)
                if "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions:
                    upload_to = app.config["UPLOAD_TO"]
                    upload_to = upload_cloudinary if upload_to == "cloudinary" \
                        else upload_imgbb if upload_to == "imgbb" else upload_local
                    recipe["image"] = upload_to(image)
                else:
                    recipe["image"] = filename
            if "created_at" in recipe:
                del recipe["created_at"]
            if "updated_at" in recipe:
                del recipe["updated_at"]
            if "deleted_at" in recipe:
                del recipe["deleted_at"]
            post = self.Recipe.load(recipe)
        except ValidationError as err:
            return self.RESPONSE.dump({
                "success": False,
                "errors": err.messages
            })
        except Exception as error:
            print(error)
            return self.RESPONSE.dump({
                "success": False,
                "message": "something error"
            }), 500
        db.session.add(post)
        db.session.commit()

        return self.recipe_schema.dump({
            "success": True,
            "message": "success add data",
            "data": post
        })

    def detail(self, recipe_id):
        recipe = RecipeModels.Recipe.query.filter_by(id=recipe_id, deleted_at=None).first()
        if not recipe:
            return self.RESPONSE.dump({
                "success": False,
                "message": f"recipe by id : {recipe_id} not found"
            }), 404
        return self.recipe_schema.dump({
            "success": True,
            "message": "success retrieve data",
            "data": recipe
        })

    def put(self, recipe_id, profile):
        recipe = RecipeModels.Recipe.query.filter_by(id=recipe_id, deleted_at=None).first()
        data = request.form if request.form else {}
        if not recipe:
            return self.RESPONSE.dump({
                "success": False,
                "message": f"recipe by id : {recipe_id} not found"
            }), 404
        if recipe.id_user != profile.id and profile.role != "admin":
            return self.RESPONSE.dump({
                "success": False,
                "message": "you not have permission to edit recipes that belong to other user!"
            }), 403
        try:
            recipe.name = data["name"] if "name" in data else recipe.name
            recipe.country = data["country"] if "country" in data else recipe.country
            recipe.category = data["category"] if "category" in data else recipe.category
            recipe.description = data["description"] if "description" in data else recipe.description
            if "image" in request.files:
                allowed_extensions = ['png', 'jpg', 'jpeg', 'gif']
                image = request.files["image"]
                filename = secure_filename(image.filename)
                if "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions:
                    upload_to = app.config["UPLOAD_TO"]
                    upload_to = upload_cloudinary if upload_to == "cloudinary" \
                        else upload_imgbb if upload_to == "imgbb" else upload_local
                    recipe.image = upload_to(image)
                else:
                    recipe.image = filename
            recipe.updated_at = db.func.now()
            post = self.Recipe.load(recipe.__dict__)
        except ValidationError as err:
            return self.RESPONSE.dump({
                "success": False,
                "errors": err.messages
            }), 400
        except Exception as error:
            print(error)
            return self.RESPONSE.dump({
                "success": False,
                "message": "something error"
            }), 500
        db.session.commit()
        post.user = User.query.filter_by(id=post.id_user).first()
        return self.recipe_schema.dump({
            "success": True,
            "message": "success update data",
            "data": post
        })

    def delete(self, recipe_id, user_data):
        user = User.query.filter_by(id=user_data.id, deleted_at=None).first()
        recipe = RecipeModels.Recipe.query.filter_by(id=recipe_id, deleted_at=None).first()
        if not recipe:
            return self.RESPONSE.error_not_found(f"recipe by id : {recipe_id} not found")
        if recipe.id_user != user.id and user.role != "admin":
            return self.RESPONSE.access_denied()
        db.session.delete(recipe)
        db.session.commit()
        return self.recipe_schema.dump({
            "success": True,
            "message": "success delete recipe",
            "data": recipe
        })
