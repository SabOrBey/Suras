from django.db import models


class Sura(models.Model):
    name = models.CharField(verbose_name="Название Суры на арабском", max_length=30, null=True, blank=True)
    transcript = models.CharField(verbose_name="Транскрипт Суры на кирилице", max_length=30, null=True, blank=True)
    translation = models.CharField(verbose_name="Перевод Суры на русский", max_length=30, null=True, blank=True)
    audio = models.FileField(verbose_name="Сура", upload_to="audio/", null=True, blank=True)
    audio_translation = models.FileField(
        verbose_name="Перевод Суры на русский", upload_to="audio/", null=True, blank=True
    )

    def __str__(self):
        return self.transcript or self.name or f"Сура {self.pk}"

    class Meta:
        ordering = ["pk"]


class Aiyat(models.Model):
    number = models.IntegerField(verbose_name="Номер Аята", null=True, blank=True)
    text = models.TextField(verbose_name="Текст Аята на арабском", null=True, blank=True)
    transcript = models.TextField(verbose_name="Транскрипт Аята на кирилице", null=True, blank=True)
    translation = models.TextField(verbose_name="Перевод Аята на русский", null=True, blank=True)
    audio_aiyat_begin = models.IntegerField(verbose_name="Начало аята", null=True, blank=True)
    audio_aiyat_end = models.IntegerField(verbose_name="Конец аята", null=True, blank=True)
    audio_aiyat_translation_begin = models.IntegerField(verbose_name="Начало перевода", null=True, blank=True)
    audio_aiyat_translation_end = models.IntegerField(verbose_name="Конец перевода", null=True, blank=True)
    learn = models.BooleanField(verbose_name="Учить", default=False)
    s_id = models.ForeignKey(Sura, on_delete=models.PROTECT, verbose_name="Сура", null=True, blank=True)

    def __str__(self):
        return f"Сура: {self.s_id}, {self.number} Аят"


class Hadith(models.Model):
    title = models.CharField("Название", max_length=200)
    arabic_text = models.TextField("Текст на арабском")
    transliteration = models.TextField("Транскрипция", blank=True)
    translation = models.TextField("Перевод")
    narrator = models.CharField("Передатчик", max_length=160, blank=True)
    source = models.CharField("Источник", max_length=200)
    audio = models.FileField("Аудиозапись", upload_to="hadith/audio/", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "хадис"
        verbose_name_plural = "хадисы"


class Dua(models.Model):
    title = models.CharField("Название", max_length=200)
    category = models.CharField("Категория", max_length=100, blank=True)
    arabic_text = models.TextField("Текст на арабском")
    transliteration = models.TextField("Транскрипция", blank=True)
    translation = models.TextField("Перевод")
    occasion = models.TextField("Когда читать", blank=True)
    source = models.CharField("Источник", max_length=200, blank=True)
    audio = models.FileField("Аудиозапись", upload_to="duas/audio/", blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order", "pk"]
        verbose_name = "дуа"
        verbose_name_plural = "дуа"
