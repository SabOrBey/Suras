from django.contrib import admin

from .models import Aiyat, Dua, Hadith, Sura


@admin.register(Sura)
class SuraAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "transcript", "translation")
    search_fields = ("name", "transcript", "translation")


@admin.register(Aiyat)
class AiyatAdmin(admin.ModelAdmin):
    list_display = ("s_id", "number", "learn")
    list_filter = ("s_id", "learn")
    search_fields = ("text", "transcript", "translation")


@admin.register(Hadith)
class HadithAdmin(admin.ModelAdmin):
    list_display = ("title", "narrator", "source", "order")
    search_fields = ("title", "arabic_text", "translation", "narrator", "source")
    ordering = ("order", "pk")


@admin.register(Dua)
class DuaAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "source", "order")
    list_filter = ("category",)
    search_fields = ("title", "arabic_text", "translation", "occasion", "source")
    ordering = ("order", "pk")
