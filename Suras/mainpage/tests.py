from django.test import Client, TestCase
from django.urls import reverse

from .models import Aiyat, Dua, Hadith, Sura


class LearningPagesTests(TestCase):
    def setUp(self):
        self.sura = Sura.objects.create(
            name="الفاتحة",
            transcript="Аль-Фатиха",
            translation="Открывающая",
            audio="audio/001.mp3",
            audio_translation="audio/translation-001.mp3",
        )
        self.ayat = Aiyat.objects.create(
            s_id=self.sura,
            number=1,
            text="بِسْمِ اللَّهِ",
            transcript="Бисмилляхи",
            translation="С именем Аллаха.",
            audio_aiyat_begin=1500,
            audio_aiyat_end=4200,
            audio_aiyat_translation_begin=500,
            audio_aiyat_translation_end=2800,
        )
        self.hadith = Hadith.objects.create(
            title="Урок хадиса",
            arabic_text="نص الحديث",
            transliteration="Транскрипция",
            translation="Перевод хадиса",
            source="Тестовый сборник",
        )
        self.dua = Dua.objects.create(
            title="Урок дуа",
            category="Учёба",
            arabic_text="نص الدعاء",
            transliteration="Транскрипция",
            translation="Перевод дуа",
            occasion="Для примера",
            source="Тестовый источник",
        )

    def test_homepage_links_to_all_four_learning_sections(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Чтение Корана")
        self.assertContains(response, "Заучивание")
        self.assertContains(response, "Хадисы")
        self.assertContains(response, "Дуа")
        self.assertContains(response, "Аль-Фатиха")

    def test_reading_page_renders_verse_audio_timestamps(self):
        response = self.client.get(reverse("detail", args=[self.sura.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Бисмилляхи")
        self.assertContains(response, 'data-audio-start="1500"')
        self.assertContains(response, 'data-audio-end="4200"')
        self.assertContains(response, "Слушать перевод")

    def test_memorized_ayat_progress_is_stored_in_each_browser_session(self):
        toggle_url = reverse("toggle_memorized_ayat", args=[self.sura.pk, self.ayat.pk])
        response = self.client.post(toggle_url)

        self.assertRedirects(response, reverse("memorize_sura", args=[self.sura.pk]))
        detail = self.client.get(reverse("memorize_sura", args=[self.sura.pk]))
        self.assertContains(detail, "Выучено · отменить")
        self.assertContains(detail, "data-audio-end=\"4200\"")

        another_browser = Client()
        other_response = another_browser.get(reverse("memorize_sura", args=[self.sura.pk]))
        self.assertContains(other_response, "Отметить выученным")
        self.assertContains(self.client.get(reverse("memorization_index")), "Выученных аятов: 1")

    def test_memorization_rejects_an_ayat_from_a_different_sura(self):
        another_sura = Sura.objects.create(transcript="Другая сура")

        response = self.client.post(
            reverse("toggle_memorized_ayat", args=[another_sura.pk, self.ayat.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_ayat_without_timestamps_is_not_presented_as_a_separate_audio_clip(self):
        Aiyat.objects.create(s_id=self.sura, number=2, text="Аят без аудиометок")

        response = self.client.get(reverse("memorize_sura", args=[self.sura.pk]))

        self.assertContains(response, "Аудиофрагмент для этого аята пока не размечен.")
        self.assertNotContains(response, 'aria-label="Слушать аят 2"')

    def test_hadith_and_dua_lessons_can_be_marked_and_unmarked(self):
        for section, lesson in (("hadith", self.hadith), ("dua", self.dua)):
            page_url = reverse("lesson_library", args=[section])
            toggle_url = reverse("toggle_lesson_completion", args=[section, lesson.pk])

            response = self.client.get(page_url)
            self.assertContains(response, lesson.title)
            self.assertContains(response, lesson.source)

            self.client.post(toggle_url)
            self.assertContains(self.client.get(page_url), "Изучено · отменить")
            self.client.post(toggle_url)
            self.assertContains(self.client.get(page_url), "Отметить изученным")

    def test_empty_hadith_and_dua_sections_explain_how_content_is_added(self):
        Hadith.objects.all().delete()
        Dua.objects.all().delete()

        for section in ("hadith", "dua"):
            response = self.client.get(reverse("lesson_library", args=[section]))

            self.assertContains(response, "Материалы скоро появятся")
            self.assertContains(response, "добавляются администратором")

    def test_completion_route_only_accepts_post(self):
        response = self.client.get(
            reverse("toggle_lesson_completion", args=["hadith", self.hadith.pk])
        )

        self.assertEqual(response.status_code, 405)
