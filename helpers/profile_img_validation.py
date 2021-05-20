from PIL import Image
from django import forms


def validate_profile_img(image):
    """
    This method checks if a a profile picture is a valid size

    @param image: description of the profile picture
    @type image: `InMemoryUploadedFile`
    """
    if not image:
        return image
    pil_img = Image.open(image)
    width, height = pil_img.size
    area = width * height
    if area > (1920 * 1080):
        raise forms.ValidationError('Selected image is too large')
    else:
        return image
