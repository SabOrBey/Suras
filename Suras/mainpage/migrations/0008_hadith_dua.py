from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainpage", "0007_alter_aiyat_audio_aiyat_begin_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Hadith",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("arabic_text", models.TextField(verbose_name="Текст на арабском")),
                ("transliteration", models.TextField(blank=True, verbose_name="Транскрипция")),
                ("translation", models.TextField(verbose_name="Перевод")),
                ("narrator", models.CharField(blank=True, max_length=160, verbose_name="Передатчик")),
                ("source", models.CharField(max_length=200, verbose_name="Источник")),
                (
                    "audio",
                    models.FileField(blank=True, upload_to="hadith/audio/", verbose_name="Аудиозапись"),
                ),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "хадис",
                "verbose_name_plural": "хадисы",
                "ordering": ["order", "pk"],
            },
        ),
        migrations.CreateModel(
            name="Dua",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="Название")),
                ("category", models.CharField(blank=True, max_length=100, verbose_name="Категория")),
                ("arabic_text", models.TextField(verbose_name="Текст на арабском")),
                ("transliteration", models.TextField(blank=True, verbose_name="Транскрипция")),
                ("translation", models.TextField(verbose_name="Перевод")),
                ("occasion", models.TextField(blank=True, verbose_name="Когда читать")),
                ("source", models.CharField(blank=True, max_length=200, verbose_name="Источник")),
                (
                    "audio",
                    models.FileField(blank=True, upload_to="duas/audio/", verbose_name="Аудиозапись"),
                ),
                ("order", models.PositiveIntegerField(default=0, verbose_name="Порядок")),
            ],
            options={
                "verbose_name": "дуа",
                "verbose_name_plural": "дуа",
                "ordering": ["order", "pk"],
            },
        ),
    ]
