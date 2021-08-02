from app import app, request
from app.controllers.RecipeController import Recipe
from app.middlewares.AuthJwt import token_required
from flask import send_from_directory

recipe = Recipe()


@app.route("/recipes", methods=["GET", "POST"])
def recipes():
    if request.method == "GET":
        return recipe.all()
    elif request.method == "POST":
        @token_required
        def add_recipe(user_data):
            return recipe.add(user_data)
        return add_recipe()


@app.route("/recipes/<int:recipe_id>", methods=["GET", "PUT", "DELETE"])
def crud_recipe(recipe_id):
    if request.method == "GET":
        return recipe.detail(recipe_id)
    elif request.method == "PUT":
        @token_required
        def edit_recipe(user_data):
            return recipe.put(recipe_id, user_data)
        return edit_recipe()
    elif request.method == "DELETE":
        @token_required
        def delete_recipe(user_data):
            return recipe.delete(recipe_id, user_data)
        return delete_recipe()


@app.route('/images/<path:name>')
def view_image(name):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"].split("/", 1)[1], name
    )
