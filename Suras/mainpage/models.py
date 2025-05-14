from django.db import models
from pydub import AudioSegment
from io import BytesIO
import base64
from pydub.utils import which

class Sura(models.Model):
    name = models.CharField(verbose_name='Название Суры на арабском', max_length=30, null=True, blank=True)
    transcript = models.CharField(verbose_name='Транскрипт Суры на кирилице', max_length=30, null=True, blank=True)
    translation = models.CharField(verbose_name='Перевод Суры на русский', max_length=30, null=True, blank=True)
    audio = models.FileField(verbose_name='Сура', upload_to='audio/', null=True, blank=True)
    audio_translation = models.FileField(verbose_name='Перевод Суры на русский', upload_to='audio/', null=True,
                                         blank=True)

    def __str__(self):
        return self.transcript

    class Meta:
        ordering = ['pk']

class Aiyat(models.Model):
    number = models.IntegerField(verbose_name='Номер Аята', null=True, blank=True)
    text = models.TextField(verbose_name='Текст Аята на арабском', null=True, blank=True)
    transcript = models.TextField(verbose_name='Транскрипт Аята на кирилице', null=True, blank=True)
    translation = models.TextField(verbose_name='Перевод Аята на русский', null=True, blank=True)
    audio_aiyat_begin = models.IntegerField(verbose_name='Начало аята', null=True, blank=True)
    audio_aiyat_end = models.IntegerField(verbose_name='Конец аята', null=True, blank=True)
    audio_aiyat_translation_begin = models.IntegerField(verbose_name='Начало перевода', null=True, blank=True)
    audio_aiyat_translation_end = models.IntegerField(verbose_name='Конец перевода', null=True, blank=True)
    learn = models.BooleanField(verbose_name='Учить', default=False)
    s_id = models.ForeignKey(Sura, on_delete=models.PROTECT, verbose_name='Сура', null=True, blank=True)

    def __str__(self):
        return f"Сура: {str(self.s_id)}, {str(self.number)} Аят"

    def audio_aiyat(self):
        AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
        AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
        AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"
        print(which("ffmpeg"))  # Должен вернуть путь к ffmpeg
        audio = AudioSegment.from_file(self.s_id.audio, format="mp3")
        segment = audio[self.audio_aiyat_begin:self.audio_aiyat_end]
        mp3_io = BytesIO()
        segment.export(mp3_io, format='mp3')
        mp3_io.seek(0)
        audio_base64 = base64.b64encode(mp3_io.read()).decode('utf-8')
        return audio_base64