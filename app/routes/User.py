from app import app, request
from app.controllers.UserController import User
from app.controllers.AuthController import Auth
from app.middlewares.AuthJwt import token_required

user = User()
auth = Auth()


@app.route("/register", methods=["POST"])
def register():
    return user.register()


@app.route("/verify-email/<token>")
def verify_email(token):
    return user.verify_email(token)


@app.route("/login", methods=["POST"])
def login():
    return auth.login()


@app.route("/users")
def users():
    return user.all()


@app.route("/users/<username>", methods=["GET", "PUT", "DELETE"])
def crud_user(username):
    if request.method == "GET":
        return user.detail(username)
    elif request.method == "PUT":
        @token_required
        def edit(user_data):
            return user.put(username, user_data)
        return edit()
    elif request.method == "DELETE":
        @token_required
        def delete(user_data):
            return user.delete(username, user_data)
        return delete()


@app.route("/profile/edit", methods=["PUT"])
@token_required
def edit_profile(user_data):
    return user.put(user_data.username)


@app.route("/profile/detail")
@token_required
def detail_profile(user_data):
    return user.detail(user_data.username)
