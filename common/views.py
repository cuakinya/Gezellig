from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from common.media import save_image, save_video, VIDEO_EXTENSIONS


@require_POST
def upload_media(request):
    """Загрузка картинок и видео из редактора постов и комментариев (локальное хранилище)"""
    if not request.me:
        return JsonResponse({"error": "Нужно войти в Клуб"}, status=403)

    # загружать могут только участники с оплаченным членством (в том числе новички, которые пишут интро)
    if request.me.is_banned or not request.me.is_active_membership:
        return JsonResponse({"error": "Загрузка доступна участникам с активным членством"}, status=403)

    media = request.FILES.get("media")
    if not media:
        return JsonResponse({"error": "Нет файла"}, status=400)

    if media.size > settings.MEDIA_UPLOAD_MAX_SIZE:
        return JsonResponse({"error": "Файл слишком большой"}, status=413)

    data = media.read()
    extension = media.name.rsplit(".", 1)[-1].lower() if "." in media.name else ""
    if extension in VIDEO_EXTENSIONS:
        url = save_video(data, media.name)
    else:
        url = save_image(data)

    if not url:
        return JsonResponse({"error": "Неподдерживаемый формат файла"}, status=400)

    return JsonResponse({"uploaded": [url]})
