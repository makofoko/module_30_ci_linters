"""
Здесь происходит логика обработки изображения
"""

from PIL import Image, ImageFilter
import os
from homework.celery_app import celery_app

RESULT_FOLDER = "results"
os.makedirs(RESULT_FOLDER, exist_ok=True)

@celery_app.task
def blur_image_task(filepath):
    img = Image.open(filepath)
    blurred = img.filter(ImageFilter.GaussianBlur(5))

    if blurred.mode == "RGBA":
        blurred = blurred.convert("RGB")

    filename = os.path.basename(filepath)
    result_path = os.path.join(RESULT_FOLDER, f"blurred_{filename}")

    if filename.lower().endswith(".png"):
        blurred.save(result_path, format="PNG")
    else:
        blurred.save(result_path, format="JPEG")

    return result_path