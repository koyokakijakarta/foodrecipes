from app import app
import random
import string
import os


def random_file(type_file):
    return "".join(random.sample(string.ascii_letters + string.digits, 32)) + "." + type_file


def upload(image):
    """
    Upload image to Local
    """
    try:
        if not os.path.isdir(app.config["UPLOAD_FOLDER"]):
            os.mkdir(app.config["UPLOAD_FOLDER"])
        filename = random_file(image.filename.rsplit(".", 1)[1])
        while os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"], filename)):
            filename = random_file()
        upload_image = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(upload_image)
    except Exception as error:
        print(error)
        return
    return upload_image.split("/", 1)[1]
