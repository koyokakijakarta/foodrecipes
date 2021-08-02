import base64
import requests
from app import app


def upload(image):
    """
    Upload image to ImgBB
    """
    try:
        payload = {
            "key": app.config["IMGBB_API_KEY"],
            "image": base64.b64encode(image.read())
        }
        upload_image = requests.post("https://api.imgbb.com/1/upload", data=payload).json()
    except Exception as error:
        print(error)
        return
    print(upload_image)
    return upload_image["data"]["url"]
