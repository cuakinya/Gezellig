# Что нужно поправить перед запуском

Список того, что сейчас стоит заглушкой, не работает без настройки или требует решения. Тексты, написанные ИИ, помечены «(придумано ИИ, TODO заменить)» — поиск по этой фразе находит их все, кроме тем писем (см. раздел 2).

Пути к файлам — ссылки на код в репозитории. Пути, начинающиеся с `/` (например, `/docs/about/`), — адреса страниц на сайте клуба, а не файлы.

## 1. Тексты, написанные ИИ — заменить своими

| Что | Где править |
| --- | --- |
| Лендинг: подзаголовок, блок «Зачем», блок «Как вступить» | [`frontend/html/landing.html`](frontend/html/landing.html) |
| О Клубе | на сайте: `/docs/about/` → редактировать (или [`posts/migrations/0039_club_docs_ai_drafts.py`](posts/migrations/0039_club_docs_ai_drafts.py) для новых установок). Письмо-приветствие ссылается на раздел `/docs/about/#enter` («с чего начать») — в тексте его нет, добавить или убрать ссылку в [`frontend/html/emails/welcome.html`](frontend/html/emails/welcome.html) |
| Наши ценности | `/docs/values/` |
| Как писать посты | `/docs/posting/` |
| Клубные чаты | `/docs/chats/` |
| Карта участников | `/docs/people/` |
| Связаться с нами | `/docs/contact/` |
| Политика обработки персональных данных — сейчас заглушка, на неё ведут подвал и согласие при вступлении | `/docs/privacy_policy/` (текст — от юриста, см. раздел 3) |
| Описание сайта (для поисковиков и превью ссылок) | godmode → настройки → `app_description` |
| Теги профиля: языки, «Я», хобби, «Для других членов Клуба я...» | [`common/data/tags.py`](common/data/tags.py), после правки — `manage.py update_tags` |

## 2. Тексты писем, бота и служебных страниц

**Переписаны ИИ из голоса Вастрика, помечены:**

- письма: [`frontend/html/emails/`](frontend/html/emails/) (вход, оплата, приглашения, модерация, удаление аккаунта);
- напоминания об окончании членства: [`frontend/messages/payments/subscription/`](frontend/messages/payments/subscription/);
- вступление, вход, интро новичка: [`frontend/html/auth/`](frontend/html/auth/), [`frontend/html/users/intro.html`](frontend/html/users/intro.html);
- сообщения о модерации, бане, удалении аккаунта: [`frontend/html/users/messages/`](frontend/html/users/messages/);
- взносы и истёкшее членство: [`frontend/html/users/edit/payments.html`](frontend/html/users/edit/payments.html), [`frontend/html/payments/`](frontend/html/payments/);
- команда клуба: [`frontend/html/pages/crew.html`](frontend/html/pages/crew.html) — разделы «Хранители атмосферы», «Организаторы», «Организаторы офлайн-встреч» показываются только когда у кого-то есть ачивка `parliament_member`, `vibe_minister` или `offline_org`, а написать им можно, только если задан чат (`TELEGRAM_PARLIAMENT_CHAT_ID`, `TELEGRAM_VIBES_CHAT_ID`, `TELEGRAM_EVENTS_CHAT_ID`);
- сообщения Telegram-бота: [`bot/config.py`](bot/config.py), [`bot/handlers/`](bot/handlers/). При замене текстов поправить и тесты с этими текстами: [`bot/tests/test_llm.py`](bot/tests/test_llm.py).

**Переписаны ИИ, но без пометки** — темы писем: [`notifications/email/users.py`](notifications/email/users.py), [`notifications/email/invites.py`](notifications/email/invites.py), [`payments/management/commands/send_subscription_notifications.py`](payments/management/commands/send_subscription_notifications.py).

**Остались голосом Вастрика, не переписаны:**

- еженедельный дайджест: [`frontend/html/emails/weekly.html`](frontend/html/emails/weekly.html), [`frontend/html/emails/weekly_og_description.html`](frontend/html/emails/weekly_og_description.html), заголовок «Клубный журнал» в [`notifications/management/commands/send_weekly_digest.py`](notifications/management/commands/send_weekly_digest.py) и [`notifications/telegram/templates/messages/weekly_digest_announce.html`](notifications/telegram/templates/messages/weekly_digest_announce.html);
- темы писем об ачивках и бейджах: [`notifications/email/achievements.py`](notifications/email/achievements.py), [`notifications/email/badges.py`](notifications/email/badges.py), [`notifications/management/commands/notify_expired_intros.py`](notifications/management/commands/notify_expired_intros.py);
- Telegram-уведомления (около 50 шаблонов): [`notifications/telegram/templates/messages/`](notifications/telegram/templates/messages/), в том числе причины отклонения постов [`notifications/telegram/templates/messages/post_rejected/`](notifications/telegram/templates/messages/post_rejected/) (про «батлы», «DYOR», гитхаб);
- настройки уведомлений, блок «Другие способы быть в курсе» («Онлайн», «Мякотка»): [`frontend/html/users/edit/notifications.html`](frontend/html/users/edit/notifications.html) — ссылки без заданных каналов ведут в никуда;
- промпт ИИ-модерации: [`ai/moderation.py`](ai/moderation.py) («ежемесячные треды мемов и поиска работы»);
- страница «API и приложения» (`/apps/`, [`frontend/html/openid/list_apps.html`](frontend/html/openid/list_apps.html)) — для программистов, ссылается на документацию движка; решить, нужна ли участникам;
- не написано: примеры хороших интро — [`frontend/html/users/intro.html`](frontend/html/users/intro.html) (`{# TODO #}` в шаблоне).

## 3. Решения, которые ещё не приняты

- [ ] **Цены** — не утверждены. Сейчас на сайте: 300 ₽ месяц, 700 ₽ три месяца, 2 600 ₽ год ([`payments/products.py`](payments/products.py) → `YOOKASSA_PRODUCTS`).
- [ ] **Аналитика** — разобраться: подключать или нет. Сейчас на сайте её нет (ни Яндекс Метрики, ни других счётчиков). Если подключать — понадобится уведомление о cookie.
- [ ] **Инвайт** — нужен ли. Сейчас: участник покупает код за 300 ₽ и дарит другу 31 день членства. Цена и срок — [`payments/products.py`](payments/products.py) → `YOOKASSA_INVITE_PRODUCT`. Если не нужен — убрать кнопку в [`frontend/html/invites/list_invites.html`](frontend/html/invites/list_invites.html).
- [ ] **Название** — одно написание. Задаётся в `.env` → `CLUB_NAME` **до первого запуска на сервере**: при первой установке оно записывается в базу (заголовок сайта, контакты). Позже — менять в godmode → настройки и в посте `/docs/contact/`.
- [ ] **Логотип** — черновик: чашка-облачко речи с сердцем + разноцветное «Хезеллих» кириллицей (шрифт Nunito, лицензия OFL). Исходники — [`frontend/static/images/logo/src/*.svg`](frontend/static/images/logo/src/), PNG и фавиконки пересобираются [`utils/build_logo.py`](utils/build_logo.py).
- [ ] **Бейджи** (благодарности за посты и комментарии за дни членства) — в базе бейджи Вастрика: «Беха», «Оффер в FAANG», «Держи долор» и др. (миграция [`badges/migrations/0002_auto_20211022_0858.py`](badges/migrations/0002_auto_20211022_0858.py), картинки [`frontend/static/images/badges/`](frontend/static/images/badges/)). Оставить часть, заменить или удалить. Код бейджа = имя картинки.
- [ ] **Модерация новичков** — карточка нового участника уходит в Telegram-чат модераторов (`TELEGRAM_ADMIN_CHAT_ID`). Без бота одобрять можно только в godmode. Решить, как модерировать.
- [ ] **Бот «Справочной»** ([`helpdeskbot/`](helpdeskbot/)) — отдельный бот для вопросов. Нужен ли. Если нет — убрать сервис [`helpdeskbot`](helpdeskbot) из [`docker-compose.production.yml`](docker-compose.production.yml) и его адрес из nginx.
- [ ] **ИИ-модерация и ИИ-ответы бота** — работают через OpenAI (`OPENAI_API_KEY`), это передача данных участников за границу (см. юр. вопросы). Включать ли. Если да — заменить в [`ai/config.py`](ai/config.py) номера постов-правил Вастрика на слаги своих документов (`about`, `values`, `posting`).
- [ ] **Stripe** — оплата скрыта, но код и страница `/monies/stripe/` остались (отвечает 404, пока Stripe не настроен). Удалить или оставить.
- [ ] **Юридические вопросы к юристу:**
  - политика ПДн (раздел 1);
  - согласие при вступлении: сейчас один чекбокс объединяет согласие на ПДн, согласие с правилами и «помню про интро» ([`frontend/html/auth/join.html`](frontend/html/auth/join.html)). Второе согласие — в форме интро, там же упомянуты cookie ([`frontend/html/users/intro.html`](frontend/html/users/intro.html));
  - «CC BY-SA» в подвале — лицензия на контент участников от Вастрика ([`frontend/html/layout.html`](frontend/html/layout.html), [`frontend/html/users/edit/data.html`](frontend/html/users/edit/data.html)). Ссылку «Сделано на движке vas3k.club» оставить: лицензия MIT требует сохранять указание авторства движка (хотя бы в [`LICENSE`](LICENSE));
  - передача данных за границу: OpenAI, Sentry, Mapbox, шрифты Google.

## 3а. Сервисы, которые передают данные за границу — проверить и решить

Для каждого: оставить (и тогда учесть в уведомлении РКН о трансграничной передаче), заменить российским или отключить.

| Сервис | Что уходит | Где в коде | Как отключить |
| --- | --- | --- | --- |
| OpenAI (США) | тексты постов, интро, вопросы к боту | [`ai/`](ai/), [`bot/handlers/llm.py`](bot/handlers/llm.py) | не задавать `OPENAI_API_KEY` |
| Telegram | имена, тексты комментариев и постов, карточки новичков для модераторов, сообщения участников боту | [`bot/`](bot/), [`helpdeskbot/`](helpdeskbot/), [`notifications/telegram/`](notifications/telegram/) | не задавать `TELEGRAM_*` (тогда модерация только в godmode) |
| Mapbox (США) | браузер участника загружает карту и стили; на карте — места участников | [`frontend/static/js/components/PeopleMap.vue`](frontend/static/js/components/PeopleMap.vue), [`frontend/html/map/people.html`](frontend/html/map/people.html), [`frontend/html/users/edit/profile.html`](frontend/html/users/edit/profile.html) | не задавать `MAPBOX_TOKEN` (карта не показывается, но стили всё равно грузятся с `api.mapbox.com` — убрать ссылки из шаблонов) |
| Sentry (США) | отчёты об ошибках, могут содержать данные запросов | [`club/settings.py`](club/settings.py) | не задавать `SENTRY_DSN` |
| Google Fonts | почтовый клиент получателя грузит шрифт из Google при открытии письма | [`frontend/html/emails/layout.html`](frontend/html/emails/layout.html) | убрать ссылку на шрифт |
| YouTube | встроенные видео в постах и превью в дайджесте — браузер грузит их с YouTube | [`frontend/html/posts/embeds/youtube.html`](frontend/html/posts/embeds/youtube.html), [`common/embeds.py`](common/embeds.py), [`frontend/html/emails/weekly.html`](frontend/html/emails/weekly.html) | оставить ссылкой вместо встраивания |
| Почта (SMTP) | адреса и письма участников | `.env` → `EMAIL_*` | выбрать российский сервис |
| Stripe, Patreon (США) | сейчас выключены, код остался | [`payments/views/stripe.py`](payments/views/stripe.py), [`authn/providers/patreon.py`](authn/providers/patreon.py) | — |

## 4. Домен

Варианты (свободны ли — проверить у регистратора):

1. `хезеллих.рф` — совпадает с названием на сайте, безопасно с точки зрения закона о русском языке;
2. `gezellig.club` — короткий и говорит, что это клуб;
3. `gezellig.ru`, `gezelligclub.ru`, `gezellig-club.ru` — запасные.

Можно взять два: кириллический как основной и латинский с переадресацией. После покупки: `APP_HOST` и `ALLOWED_HOSTS` (см. раздел 9 — на сервере `APP_HOST` сейчас перекрывается файлом compose), домен и пути к сертификатам в [`etc/nginx/club.conf`](etc/nginx/club.conf). Домен лучше выбрать до запуска: ссылки на загруженные картинки содержат адрес сайта.

## 5. Логотип и требования закона

С 1 марта 2026 действует ФЗ-168: на сайтах и вывесках для потребителей текст должен быть на русском, иностранный допускается только как равнозначный дубль после русского. Иностранное слово без перевода можно, если оно зарегистрировано как товарный знак (регистрация около года; у ИП нет фирменного наименования, поэтому через ЕГРЮЛ не получится).

Поэтому в логотипе и на сайте основное название — «Хезеллих» кириллицей; «gezellig» — только вторым, тем же размером и шрифтом. Уточнить у юриста, нужно ли пояснение слова (сейчас на лендинге написано, что оно значит). Латинского «Gezellig» в логотипе нет.

Файлы логотипа: [`frontend/static/images/logo/`](frontend/static/images/logo/), фавиконки: [`frontend/static/images/favicon/`](frontend/static/images/favicon/), превью для соцсетей: [`frontend/static/images/share.png`](frontend/static/images/share.png).

## 6. Почта

Нужны две вещи:

1. **Почтовый ящик на домене** для писем от людей: `club@домен` (контакты), можно отдельно `moderator@` и `pay@`. Подключается у почтового сервиса для домена (например, Яндекс 360 для бизнеса или VK WorkSpace). Адреса — в `.env`: `CLUB_CONTACT_EMAIL`, `CLUB_MODERATOR_EMAIL`, `CLUB_PAYMENTS_EMAIL` — **задать до первого запуска на сервере** (записываются в базу: пост «Связаться с нами», служебный пользователь moderator).
2. **Сервис отправки писем (SMTP)**, через который сайт сам шлёт письма. Это критично: **вход на сайт — по коду из письма**, без настроенной отправки участники не смогут войти. Также письма об оплате и восстановлении доступа. В `.env`: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`. На домене настроить SPF, DKIM и DMARC, иначе письма уйдут в спам.

Пока `EMAIL_HOST` пустой, письма и коды входа печатаются в консоль: без Docker — в окне `manage.py qcluster`, в Docker — в логах контейнера `queue`. Для локальной проверки этого достаточно. **На сервере забытый SMTP не вызывает ошибки** — письма молча уйдут в лог, поэтому после запуска проверить вход с реальной почтой.

## 7. Оплата

- [ ] Тестовый магазин ЮKassa → ключи в `.env` → пройти оплату тестовой картой.
- [ ] Боевой магазин после регистрации ИП и договора.
- [ ] Webhook в кабинете ЮKassa: `https://домен/monies/yookassa/webhook/`, событие `payment.succeeded`.
- [ ] Чек: в [`payments/views/yookassa.py`](payments/views/yookassa.py) стоят «услуга» и «без НДС», система налогообложения (`tax_system_code`) не передаётся — сверить с налоговым режимом и с тем, как ЮKassa работает с самозанятыми (чеки через «Мой налог»).

## 8. Telegram, сервисы и наполнение

- [ ] **Бот клуба**: создать в BotFather, вписать в `.env` `TELEGRAM_TOKEN`, **адрес бота** `TELEGRAM_BOT_URL` (`https://t.me/имя_бота`) и `TELEGRAM_ADMIN_CHAT_ID` — без него бот не запускается. Без адреса бот не узнаёт, что к нему обращаются через @, и не отвечает на упоминания в чатах.
- [ ] Каналы и чаты клуба: `TELEGRAM_CLUB_CHANNEL_URL`, `TELEGRAM_CLUB_CHANNEL_ID`, `TELEGRAM_CLUB_CHAT_ID`, `TELEGRAM_ONLINE_CHANNEL_URL`, `TELEGRAM_ONLINE_CHANNEL_ID`, `TELEGRAM_BEST_COMMENTS_CHANNEL_ID`, `TELEGRAM_VIBES_CHAT_ID`, `TELEGRAM_PARLIAMENT_CHAT_ID`, `TELEGRAM_EVENTS_CHAT_ID`. Незаданные просто отключают свою функцию.
- [ ] Бот «Справочной», если нужен: `TELEGRAM_HELP_DESK_BOT_TOKEN` и др. ([`helpdeskbot/config.py`](helpdeskbot/config.py)) — без него сервис [`helpdeskbot`](helpdeskbot) на сервере падает.
- [ ] Карта участников: свой токен Mapbox → `MAPBOX_TOKEN` (и при желании `MAPBOX_STYLE`). Проверить, что Mapbox доступен из России; если нет — карту отключить или заменить.
- [ ] **Комнаты** (`/rooms/`, разделы по темам) — создать в godmode. Шаблоны уже ссылаются на комнаты `questions` («Справочная») и `best_comments`, без них ссылки ведут на 404.
- [ ] **Сеть чатов** (`/network/`) — пусто, наполняется в godmode.
- [ ] **Ачивки клуба**: [`common/data/achievements.py`](common/data/achievements.py) (сейчас пусто). Команда `update_achievements` удаляет из базы ачивки, которых нет в списке.
- [ ] Коллекционные теги — создаются только в godmode, сейчас их нет.
- [ ] Календарь событий наполняется постами типа «событие» — пуст до первых встреч.
- [ ] Необязательные переменные, можно не задавать: `SENTRY_DSN` (отчёты об ошибках), `JWT_PRIVATE_KEY` и `JWT_PUBLIC_KEY` (вход «через клуб» в сторонних сервисах, страница `/apps/`), `WEBHOOK_SECRETS` (входящие вебхуки от сторонних сервисов), `OPENAI_API_KEY` (см. раздел 3).

## 9. Сервер

**Что должно работать** ([`docker-compose.production.yml`](docker-compose.production.yml)): сайт `club_app`, очередь `queue` (без неё не уходят письма и коды входа), `cron` (рассылки, напоминания об окончании членства, удаление аккаунтов, пересчёт ленты — расписание в [`etc/crontab`](etc/crontab), время в UTC), `redis`, боты [`bot`](bot) и [`helpdeskbot`](helpdeskbot). PostgreSQL в compose нет — ставится на сервер отдельно.

- [ ] **`APP_HOST` в [`docker-compose.production.yml`](docker-compose.production.yml) жёстко задан как `https://club.example.com`** и перекрывает значение из `.env` — заменить на свой домен или убрать из compose. Иначе все ссылки в письмах, платежах и боте будут вести не туда.
- [ ] **Образ** `ghcr.io/cuakinya/gezellig` в compose никто не собирает и не публикует — собрать самостоятельно или заменить `image:` на `build:`.
- [ ] PostgreSQL на сервере: пользователь [`club`](club) и база `hezellikh` (заданы в compose), свой пароль `POSTGRES_PASSWORD` (в [`.env.example`](.env.example) стоит `postgres`).
- [ ] `.env` для продакшена: свой `SECRET_KEY` (без него сайт запустится на общеизвестном ключе `wow so secret` — ошибки не будет), `ALLOWED_HOSTS`, `DEBUG=false` (уже стоит в compose), название и адреса клуба (раздел 3 и 6) — до первого запуска.
- [ ] **Первый администратор.** Служебный вход `/godmode/dev_login/` на сервере не работает. Создать пользователя с ролью god через `manage.py shell` (email, slug, `roles=["god"]`, `moderation_status="approved"`, `is_email_verified=True`, `membership_expires_at` в будущем) — инструкция по смыслу в [`docs/tech_guide.md`](docs/tech_guide.md), но она предполагает обычную регистрацию с оплатой.
- [ ] **Теги профиля на сервере** не загружаются автоматически: после первого запуска выполнить `manage.py update_tags` (при запуске выполняются только миграции и `update_achievements`).
- [ ] Бэкапы базы и папки `media/`.
- [ ] nginx по примеру [`etc/nginx/club.conf`](etc/nginx/club.conf) (заменить домен и пути `/home/club/...`), сертификат HTTPS.
- [ ] Для HTTPS включить защищённые cookie (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`) и HSTS — сейчас в [`club/settings.py`](club/settings.py) их нет.
- [ ] CSRF-защиты форм в движке нет (так и у оригинала) — обсудить с разработчиком.
- [ ] Ограничение частоты загрузок файлов (`/upload/`, до 20 МБ за раз) — сейчас нет, можно задать в nginx.
