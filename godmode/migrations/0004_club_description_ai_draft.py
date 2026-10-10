from django.db import migrations


def forwards(apps, schema_editor):
    ClubSettings = apps.get_model("godmode", "ClubSettings")
    ClubSettings.objects.update_or_create(
        code="app_description",
        defaults={"value": "(придумано ИИ, TODO заменить) Закрытый клуб для тех, кто учит языки"},
    )


class Migration(migrations.Migration):

    dependencies = [
        ("godmode", "0003_club_branding"),
    ]

    operations = [
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
