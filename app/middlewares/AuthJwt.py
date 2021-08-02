import jwt
import datetime
from functools import wraps
from hashlib import md5
from app import app, request
from app.models import User as UserModels
from app.schemas.Response import ResponseSchema

RESPONSE = ResponseSchema()


def encode(username, password):
    payload = {
        "username": username,
        "password": password,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=10)
    }
    token = jwt.encode(payload, app.config["JWT_SECRET"], algorithm="HS256")
    return token


def decode(token):
    return jwt.decode(token, app.config["JWT_SECRET"], algorithms=["HS256"])


def token_required(fun):
    @wraps(fun)
    def decorator(**kwargs):
        if "Authorization" in request.headers:
            try:
                token = request.headers["Authorization"]
                auth = decode(token)
            except jwt.exceptions.DecodeError:
                return RESPONSE.dump({
                    "success": False,
                    "message": "token required"
                }), 401
            except jwt.exceptions.ExpiredSignatureError:
                return RESPONSE.dump({
                    "success": False,
                    "message": "token expired"
                }), 401
            if "username" in auth and "password" in auth:
                user = UserModels.User.query.filter_by(
                    username=auth["username"],
                    active="Y",
                    deleted_at=None
                ).first()
                if not user:
                    return RESPONSE.dump({
                        "success": False,
                        "message": "user %r in token not found" % auth["username"]
                    }), 401
                salt = user.salt
                user_password = user.password
                passw = auth["password"]+salt
                password_encrypt = md5(passw.encode()).hexdigest()
                if user_password != password_encrypt:
                    return RESPONSE.dump({
                        "success": False,
                        "message": "password in token unmatch"
                    }), 401
                return fun(user_data=user, **kwargs)
            else:
                return RESPONSE.dump({
                    "success": False,
                    "message": "token required"
                }), 401
        else:
            return RESPONSE.dump({
                "success": False,
                "message": "token required"
            }), 401
    return decorator
