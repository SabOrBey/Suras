from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

urlpatterns = [
    path("experiment", views.experiment, name="experiment"),
    path("memorize/", views.memorization_index, name="memorization_index"),
    path("memorize/<int:sura_id>/", views.memorize_sura, name="memorize_sura"),
    path(
        "memorize/<int:sura_id>/<int:ayat_id>/",
        views.toggle_memorized_ayat,
        name="toggle_memorized_ayat",
    ),
    path("lessons/<slug:section>/", views.lesson_library, name="lesson_library"),
    path(
        "lessons/<slug:section>/<int:lesson_id>/",
        views.toggle_lesson_completion,
        name="toggle_lesson_completion",
    ),
    path("<int:sura_id>/", views.detail, name="detail"),
    path("", views.index, name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
