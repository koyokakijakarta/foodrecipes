from flask import request
from app.models.User import User
from app.schemas.Response import ResponseSchema
from app.middlewares import AuthJwt
import hashlib
import string
import random


class Auth:
    RESPONSE = ResponseSchema()

    @staticmethod
    def encrypt(password):
        salt = "".join(random.sample(string.ascii_letters, 32))
        new_password = password+salt
        return hashlib.md5(new_password.encode()).hexdigest(), salt
    
    def login(self):
        if not request.json or not all(x in request.json for x in ["username", "password"]):
            return self.RESPONSE.dump({
                "success": False,
                "message": "please complete the input data"
            }), 400
        username, password = request.json["username"], request.json["password"]
        get_user = User.query.filter_by(username=username).first()
        if not get_user:
            return self.RESPONSE.dump({
                "success": False,
                "message": "user not found"
            }), 404
        salt = get_user.salt
        user_password = get_user.password
        passw = password+salt
        password_encrypt = hashlib.md5(passw.encode()).hexdigest()
        if user_password != password_encrypt:
            return self.RESPONSE.dump({
                "success": False,
                "message": "password unmatch"
            }), 401
        return self.RESPONSE.dump({
            "token": AuthJwt.encode(username, password),
            "message": "success login"
        })
