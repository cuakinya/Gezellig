# Хезеллих

Платформа клуба для полиглотов. Работает на движке [vas3k.club](https://github.com/vas3k/vas3k.club) (лицензия MIT) — копия движка на коммите `8305ac0` от 1 октября 2026, отвязанная от инфраструктуры Вастрик.Клуба.

Стек: Django, PostgreSQL, Redis, Vue-компоненты внутри Django-шаблонов, Webpack, uv.

## Запуск на своём компьютере

### Через Docker (проще всего)

```sh
cp .env.example .env
docker compose up
```

Сайт откроется на http://127.0.0.1:8000.

### Без Docker

Нужны [uv](https://docs.astral.sh/uv/) (он сам поставит Python 3.14), Node 22+, PostgreSQL и Redis.

```sh
cp .env.example .env                 # проверить POSTGRES_* и REDIS_HOST
createdb hezellikh
uv sync
npm ci --prefix frontend && npm run build --prefix frontend
uv run python manage.py migrate
uv run python manage.py update_tags
uv run python manage.py runserver    # сайт
uv run python manage.py qcluster     # очередь задач (письма, уведомления) — в отдельном окне
```

Пока в `.env` не задан `EMAIL_HOST`, письма никуда не отправляются, а печатаются в окне `qcluster` — там же код для входа (в теме письма). Если запускаете сайт не на порту 8000, поправьте `APP_HOST` — из него строятся ссылки в письмах и платежах.

### Войти

В режиме `DEBUG=true` работают служебные входы:

- http://127.0.0.1:8000/godmode/dev_login/ — администратор (роль god) с оплаченным членством;
- http://127.0.0.1:8000/godmode/random_login/ — случайный новый участник.

Админка — `/godmode/`.

## Что настраивается и где

| Что | Где |
| --- | --- |
| Название клуба, контактные адреса | `.env`: `CLUB_NAME`, `CLUB_*_EMAIL` |
| Заголовок и описание сайта | godmode → настройки (`app_name`, `app_title`, `app_description`) |
| Тарифы и цены | `payments/products.py` → `YOOKASSA_PRODUCTS` |
| Оплата | `.env`: `YOOKASSA_SHOP_ID`, `YOOKASSA_API_KEY` |
| Почта | `.env`: `EMAIL_*`, `DEFAULT_FROM_EMAIL` |
| Telegram-бот и каналы | `.env`: `TELEGRAM_*` |
| Карта участников | `.env`: `MAPBOX_TOKEN`, `MAPBOX_STYLE` |
| Включение/выключение функций | `club/features.py` |
| Тексты «О Клубе», ценности, политика, контакты | посты типа «Доки» (`/docs/about/` и т.д.), правятся на сайте |
| Ачивки | `common/data/achievements.py` (сейчас пусто), затем `manage.py update_achievements` |
| Логотип и фавиконки | `frontend/static/images/logo/`, `frontend/static/images/favicon/` |

В шаблонах название и адреса берутся тегами `{% club_name %}`, `{% club_url %}`, `{% club_email %}` — они работают везде без `{% load %}`, в том числе в письмах.

## Оплата

Только ЮKassa, разовые покупки: месяц — 300 ₽, 3 месяца — 700 ₽, год — 2600 ₽, без автопродления: новые дни прибавляются к текущему сроку. Инвайт для друга покупается там же.

- Без ключей ЮKassa страница оплаты показывает «Оплата ещё не настроена».
- Для проверки без договора: зарегистрироваться в ЮKassa, создать тестовый магазин, вписать его `shopId` и секретный ключ в `.env`. Тестовая карта: `4111 1111 1111 1111`, срок — любая будущая дата, CVC — любой.
- Webhook для подтверждения оплаты: `https://ваш-домен/monies/yookassa/webhook/` (событие `payment.succeeded`). Локально ЮKassa до него не достучится — нужен публичный адрес.
- Код Stripe из движка оставлен, но из интерфейса убран (`/monies/stripe/`).

## Картинки

Загрузки из редактора (`POST /upload/`) и аватары сохраняются на этом же сервере в `media/`. Картинки пересохраняются (это убирает EXIF с геолокацией) и уменьшаются до 2560 px. Локально их раздаёт Django, на сервере — nginx (пример в `etc/nginx/club.conf`).

## Что осталось заглушкой

Полный список с местами в коде — [TODO.md](TODO.md). Тексты, написанные ИИ, помечены на сайте «(придумано ИИ, TODO заменить)».

## Тесты

```sh
TESTS_RUN=true uv run python manage.py test   # нужны запущенные Postgres и Redis
npm test --prefix frontend
```

## Обновления движка

Оригинальный репозиторий подключён как `upstream`, если склонировать так:

```sh
git remote add upstream https://github.com/vas3k/vas3k.club
git fetch upstream
```

История этого репозитория начинается со снимка движка, поэтому изменения из upstream переносятся вручную (`git diff 8305ac0 upstream/master` по нужным файлам).

## Благодарности

Движок — [vas3k.club](https://github.com/vas3k/vas3k.club), © Vasily Zubarev, лицензия MIT (см. `LICENSE`). Оригинальный README — [docs/UPSTREAM_README.md](docs/UPSTREAM_README.md), техническая документация движка — в `docs/`.
