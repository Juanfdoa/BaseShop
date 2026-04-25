import cloudinary
import cloudinary.uploader

def upload_image(image):
    if image.filename == "":
        return "Image error."
 
    result = cloudinary.uploader.upload(
        image,
        folder="mi_app", 
        resource_type="image"
    )
    
    return result["secure_url"] 