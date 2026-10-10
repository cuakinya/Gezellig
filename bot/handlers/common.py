import logging
from enum import Enum
from typing import Optional

from django.conf import settings
from telegram import Update
from telegram.constants import ParseMode

from bot.config import COMMENT_URL_RE, POST_URL_RE
from comments.models import Comment
from posts.models.post import Post
from users.models.user import User

log = logging.getLogger(__name__)


class UserRejectReason(Enum):
    intro = "intro"
    data = "data"
    ai = "ai"
    aggression = "aggression"
    general = "general"
    name = "name"


class PostRejectReason(Enum):
    title = "title"
    design = "design"
    dyor = "dyor"
    duplicate = "duplicate"
    chat = "chat"
    tldr = "tldr"
    github = "github"
    bias = "bias"
    hot = "hot"
    ad = "ad"
    inside = "inside"
    value = "value"
    draft = "draft"
    false_dilemma = "false_dilemma"


async def get_club_user(update: Update):
    user = User.objects.filter(telegram_id=update.effective_user.id).first()
    if not user:
        if update.callback_query:
            await update.callback_query.answer(text=f"☝️ (придумано ИИ, TODO заменить) Привяжите бота к профилю")
        else:
            await update.message.reply_text(
                f"😐 (придумано ИИ, TODO заменить) Привяжите <a href=\"{settings.APP_HOST}/user/me/edit/bot/\">бота</a> к профилю",
                parse_mode=ParseMode.HTML
            )
        return None

    if user.is_banned:
        if update.callback_query:
            await update.callback_query.answer(text=f"🙈 (придумано ИИ, TODO заменить) Ваш аккаунт заблокирован")
        else:
            await update.message.reply_text(f"🙈 (придумано ИИ, TODO заменить) Ваш аккаунт заблокирован")
        return None

    if not user.is_member:
        if update.callback_query:
            await update.callback_query.answer(text=f"😣 (придумано ИИ, TODO заменить) Срок вашего членства в Клубе закончился. Продлите его, чтобы пользоваться ботом")
        else:
            await update.message.reply_text(f"😣 (придумано ИИ, TODO заменить) Срок вашего членства в Клубе закончился. Продлите его, чтобы пользоваться ботом")
        return None

    return user


async def get_club_comment(update: Update) -> Optional[Comment]:
    entities = update.message.reply_to_message.entities or update.message.reply_to_message.caption_entities or []
    url_entities = [
        entity.url for entity in entities if entity.type == "text_link"
    ]

    for url_entity in url_entities:
        match = COMMENT_URL_RE.match(url_entity)
        if match:
            comment_id = match.group(1)
            if comment_id:
                break
    else:
        log.warning(f"Comment URL not found in message: {update.message.reply_to_message}")
        return None

    comment = Comment.objects.filter(id=comment_id).first()
    if not comment:
        await update.message.reply_text(f"🤨 (придумано ИИ, TODO заменить) Комментарий '{comment_id}' не найден: возможно, он был удалён")
        return None

    return comment


async def get_club_post(update: Update) -> Optional[Post]:
    entities = update.message.reply_to_message.entities or update.message.reply_to_message.caption_entities or []
    url_entities = [
        entity.url for entity in entities if entity.type == "text_link"
    ]

    for url_entity in url_entities:
        match = POST_URL_RE.match(url_entity)
        if match:
            post_id = match.group(1)
            if post_id:
                break
    else:
        log.warning(f"Post URL not found in message: {update.message.reply_to_message}")
        return None

    post = Post.objects.filter(slug=post_id).first()
    if not post or not post.is_commentable:
        await update.message.reply_text(f"🤨 (придумано ИИ, TODO заменить) Пост не найден: возможно, он был удалён или скрыт")
        return None

    return post
