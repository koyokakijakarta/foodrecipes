import cloudinary
from app import app
from cloudinary import uploader

cloudinary.config(
    cloud_name=app.config["CLOUDINARY_NAME"],
    api_key=app.config["CLOUDINARY_API_KEY"],
    api_secret=app.config["CLOUDINARY_API_SECRET"]
)


def upload(image):
    """
    Upload image to Cloudinary
    """
    try:
        upload_image = uploader.upload(image)
    except Exception as error:
        print(error)
        return
    print(upload_image)
    return upload_image["secure_url"]
