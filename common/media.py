"""
Локальное хранилище картинок и видео.

У Вастрика загрузки уходят на отдельный сервис i.vas3k.club. Здесь по умолчанию
(MEDIA_UPLOAD_URL начинается с "/") файлы кладутся в MEDIA_ROOT на этом же сервере
и раздаются по MEDIA_URL: в DEBUG — самим Django, в продакшене — nginx.
"""
import hashlib
import io
import logging
import os

from PIL import Image, ImageOps
from django.conf import settings

log = logging.getLogger(__name__)

IMAGE_MAX_SIDE = 2560
IMAGE_FORMATS = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp", "GIF": "gif"}
VIDEO_EXTENSIONS = {"mp4", "mov", "webm"}


def is_local_storage():
    return not settings.MEDIA_UPLOAD_URL or settings.MEDIA_UPLOAD_URL.startswith("/")


def _store(data: bytes, extension: str) -> str:
    name = hashlib.sha256(data).hexdigest()[:40] + "." + extension
    path = os.path.join(settings.MEDIA_ROOT, name[:2], name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "wb") as f:
            f.write(data)
    return f"{settings.APP_HOST}{settings.MEDIA_URL}{name[:2]}/{name}"


def save_image(data: bytes, resize=None, convert_to=None, quality=None) -> str | None:
    """Пересохраняет картинку (это заодно убирает EXIF с геолокацией) и возвращает её публичный URL"""
    try:
        image = Image.open(io.BytesIO(data))
        source_format = image.format
        image.load()
    except Exception as ex:
        log.warning(f"Bad image data: {ex}")
        return None

    if source_format not in IMAGE_FORMATS:
        return None

    # анимированные гифки не трогаем, иначе останется один кадр
    if source_format == "GIF" and getattr(image, "is_animated", False) and not resize and not convert_to:
        return _store(data, "gif")

    image = ImageOps.exif_transpose(image)
    image.thumbnail(resize or (IMAGE_MAX_SIDE, IMAGE_MAX_SIDE))

    extension = (convert_to or IMAGE_FORMATS[source_format]).lower().replace("jpeg", "jpg")
    save_format = {"jpg": "JPEG", "png": "PNG", "webp": "WEBP", "gif": "GIF"}.get(extension)
    if not save_format:
        return None
    if save_format == "JPEG" and image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    output = io.BytesIO()
    image.save(output, format=save_format, quality=int(quality or 90))
    return _store(output.getvalue(), extension)


def save_video(data: bytes, filename: str) -> str | None:
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in VIDEO_EXTENSIONS:
        return None
    return _store(data, extension)
