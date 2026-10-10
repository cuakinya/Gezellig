import re
from urllib.parse import urlparse

from django.conf import settings

CLUB_HOST_RE = re.escape(urlparse(settings.APP_HOST).netloc)
BOT_PROFILE_URL = f"{settings.APP_HOST}/user/me/edit/bot/"

WELCOME_MESSAGE = f"""✖️ <b>(придумано ИИ, TODO заменить) Я — бот клуба «{settings.CLUB_NAME}»</b>\n
Через меня можно отвечать на комментарии и посты: просто ответьте реплаем на сообщение, и я опубликую ваш ответ в Клубе.
Так можно участвовать в обсуждениях, не открывая сайт.\n
Ещё во мне есть ИИ-помощник, который умеет искать и подсказывать информацию по материалам Клуба.\n
Вот команды, которые я знаю:
/top - Топ событий в Клубе
/random - Случайный пост из Клуба
/whois - Узнать профиль по телеграму
/horo - Клубный гороскоп
/auth - Привязать бота к аккаунту в Клубе
/help - Справка"""

ANONYMOUS_MESSAGE = f"""(придумано ИИ, TODO заменить) Здравствуйте! Мы пока не знакомы. Привяжите меня к аккаунту командой /auth с
<a href=\"{BOT_PROFILE_URL}\">кодом из профиля</a> через пробел"""

BOT_USERNAME = settings.TELEGRAM_BOT_URL.rstrip("/").rsplit("/", 1).pop() if settings.TELEGRAM_BOT_URL else ""
# без настроенного бота паттерн не должен ловить любое упоминание через @
BOT_MENTION_RE = re.compile(rf"@{re.escape(BOT_USERNAME)}\b" if BOT_USERNAME else r"(?!x)x", re.IGNORECASE)

MIN_COMMENT_LEN = 40
SKIP_COMMANDS = ("/skip", "/Skip", "#skip", "#ignore")
COMMENT_EMOJI_RE = re.compile(r"^💬.*")
POST_EMOJI_RE = re.compile(r"^[📝🔗❓💡🏢🤜🤛🗺🗄🔥🏗🙋‍♀️].*")
COMMENT_URL_RE = re.compile(rf"https?://{CLUB_HOST_RE}/[a-zA-Z]+/.+?/#comment-([a-fA-F0-9\-]+)")
POST_URL_RE = re.compile(rf"https?://{CLUB_HOST_RE}/[a-zA-Z]+/(.+?)/")
