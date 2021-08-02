from app import app, request, celery, db, mail, Message
from app.models import User as UserModels, Recipe
from app.schemas.User import User, UserAll, UserDetail
from app.controllers.AuthController import Auth
from app.schemas.Response import ResponseSchema
from marshmallow import ValidationError
import string
import random


@celery.task(name="app.send_email_verification")
def send_email(url_root, user):
    with app.app_context():
        link = url_root + "verify-email/" + user["token"]
        msg = Message(
            "Welcome to Food Recipes Apps",
            sender=("Food Recipes Apps", app.config["MAIL_DEFAULT_SENDER"]),
            recipients=[user["email"]]
        )
        msg.html = f"""
            <h1>Welcome { user["fullname"] }! Thanks for signing up.</h1>
            <p>
                Please follow this link to activate your account.
                If you didn't issue a password reset you can safely ignore this email.
            </p>
            <a href="{ link }">{ link }</a>
        """
        mail.send(msg)


class User:
    RESPONSE = ResponseSchema()
    users_schema = UserAll()
    user_schema = UserDetail()
    User = User()

    def register(self):
        data = request.form
        user = UserModels.User.query.filter_by(username=data["username"]).first()
        if user:
            return self.RESPONSE.dump({
                "success": False,
                "message": "username is already used!"
            }), 409
        auth = Auth()
        try:
            user = data.copy()
            user["password"], user["salt"] = auth.encrypt(user["password"])
            user["role"] = "user"
            user["token"] = "".join(random.sample(string.ascii_letters, 32))
            if "active" in user:
                del user["active"]
            if "created_at" in user:
                del user["created_at"]
            if "updated_at" in user:
                del user["updated_at"]
            if "deleted_at" in user:
                del user["deleted_at"]
            post = self.User.load(user)

            send_email.delay(request.url_root, user)
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

        db.session.add(post)
        db.session.commit()
        return self.user_schema.dump({
            "success": True,
            "message": "check your email for verification!",
            "data": post
        }), 201

    def verify_email(self, token):
        user = UserModels.User.query.filter_by(token=token, active="N").first()
        if not user:
            return self.RESPONSE.dump({
                "success": False,
                "message": "invalid token!"
            }), 401
        user.active = "Y"
        db.session.commit()
        return self.user_schema.dump({
            "success": True,
            "message": "success verify email!",
            "data": user
        })

    def all(self):
        users = UserModels.User.query.filter_by(active="Y", deleted_at=None).order_by(UserModels.User.id)
        if request.args.get("username"):
            users = users.filter(UserModels.User.username.like(f"%{request.args.get('username')}%"))
        if request.args.get("fullname"):
            users = users.filter(UserModels.User.fullname.like(f"%{request.args.get('fullname')}%"))
        if request.args.get("email"):
            users = users.filter(UserModels.User.email.like(f"%{request.args.get('email')}%"))
        return self.users_schema.dump({
            "success": True,
            "message": "success retrieve data",
            "data": users.all()
        })

    def detail(self, username):
        user = UserModels.User.query.filter_by(username=username, deleted_at=None).first()
        if not user:
            return self.RESPONSE.dump({
                "success": False,
                "message": f"user {username} not found"
            }), 404
        return self.user_schema.dump({
            "success": True,
            "message": "success retrieve data",
            "data": user
        })

    def put(self, username, user_data):
        profile = user_data
        user = profile if username == profile.username \
            else UserModels.User.query.filter_by(username=username, deleted_at=None).first()
        data = request.json
        if not user:
            return self.RESPONSE.dump({
                "success": False,
                "message": f"user {username} not found"
            }), 404
        if username != profile.username and profile.role != "admin":
            return self.RESPONSE.dump({
                "success": False,
                "message": "you not have permission to edit other user!"
            }), 403
        if UserModels.User.query.filter_by(username=data["username"]).first():
            return self.RESPONSE.dump({
                "success": False,
                "message": "username is already used!"
            }), 409
        try:
            user.fullname = data["fullname"] if "fullname" in data else user.fullname
            user.username = data["username"] if "username" in data else user.username
            user.email = data["email"] if "email" in data else user.email
            if "password" in data:
                auth = Auth()
                user.password, user.salt = auth.encrypt(data["password"])
            user.updated_at = db.func.now()
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
        return self.user_schema.dump({
            "success": True,
            "message": "success update data",
            "data": profile
        })

    def delete(self, username, user_data):
        profile = user_data
        user = profile if username == profile.username \
            else UserModels.User.query.filter_by(username=username, deleted_at=None).first()
        if not user:
            return self.RESPONSE.dump({
                "success": False,
                "message": f"user {username} not found"
            }), 404
        if username != profile.username and profile.role != "admin":
            return self.RESPONSE.dump({
                "success": False,
                "message": "you not have permission to delete other user!"
            }), 403
        user.deleted_at = db.func.now()
        recipes = Recipe.Recipe.query.filter_by(id_user=user.id)
        for recipe in recipes:
            recipe.deleted_at = db.func.now()
        db.session.commit()
        return self.user_schema.dump({
            "success": True,
            "message": f"success remove user { username }",
            "data": user
        })
