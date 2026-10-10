# Миграция 0002 записывает в настройки название и описание Вастрик.Клуба — заменяем на свои.
# Дальше их можно менять в godmode без кода.
from django.conf import settings
from django.db import migrations


def forwards(apps, schema_editor):
    ClubSettings = apps.get_model("godmode", "ClubSettings")
    values = {
        "app_name": settings.CLUB_NAME,
        "app_title": settings.CLUB_NAME,
        "app_description": "Клуб для тех, кто учит языки",
    }
    for code, value in values.items():
        ClubSettings.objects.update_or_create(code=code, defaults={"value": value})


class Migration(migrations.Migration):

    dependencies = [
        ("godmode", "0002_remove_clubsettings_digest_intro_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
