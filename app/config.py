from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(filename=".env"))
import os


class Config:
    UPLOAD_TO = os.getenv("UPLOAD_TO").lower()
    UPLOAD_FOLDER = "app/%s/" % os.getenv("UPLOAD_FOLDER")

    CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")

    JWT_SECRET = os.getenv("JWT_SECRET")
