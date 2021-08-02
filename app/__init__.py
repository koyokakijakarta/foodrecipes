from flask import Flask, request
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.from_object("app.config.Config")

celery = Celery(
    app.import_name,
    backend=app.config["CELERY_RESULT_BACKEND"],
    broker=app.config["CELERY_BROKER_URL"]
)
celery.conf.update(app.config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db, "app/migrations")
mail = Mail(app)
app.extensions['mail'].debug = 0

from app.models import Recipe, User
from app.routes import Recipe, User
