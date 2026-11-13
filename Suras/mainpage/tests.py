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

    def test_homepage_marks_reading_as_in_development_and_links_to_memorization(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Чтение Корана")
        self.assertContains(response, "Страница на разработке")
        self.assertContains(response, "Заучивание")
        self.assertContains(response, "Хадисы")
        self.assertContains(response, "Дуа")
        self.assertNotContains(response, "Суры Корана")

    def test_old_sura_detail_route_redirects_to_memorization(self):
        response = self.client.get(reverse("detail", args=[self.sura.pk]))

        self.assertRedirects(response, reverse("memorize_sura", args=[self.sura.pk]))

    def test_memorization_shows_only_selected_ayat_and_limits_audio_to_them(self):
        second_ayat = Aiyat.objects.create(
            s_id=self.sura,
            number=2,
            text="الْحَمْدُ لِلَّهِ",
            audio_aiyat_begin=4200,
            audio_aiyat_end=6700,
        )
        Aiyat.objects.create(s_id=self.sura, number=3, text="Аят вне выбранного диапазона")

        response = self.client.get(
            reverse("memorize_sura", args=[self.sura.pk]),
            {"begin": 1, "end": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Аяты 1–2")
        self.assertContains(response, "Бисмилляхи")
        self.assertContains(response, second_ayat.text)
        self.assertNotContains(response, "Аят вне выбранного диапазона")
        self.assertContains(response, 'data-clip-start-ms="1500"')
        self.assertContains(response, 'data-clip-end-ms="6700"')
        self.assertContains(response, "Повторять выбранный диапазон")
        self.assertContains(response, '<option value="3" selected>3 раза</option>')
        self.assertContains(response, "Слушать выбранный фрагмент")

        toggle_url = reverse("toggle_memorized_ayat", args=[self.sura.pk, second_ayat.pk])
        toggle_response = self.client.post(f"{toggle_url}?begin=1&end=2")

        self.assertRedirects(
            toggle_response,
            f"{reverse('memorize_sura', args=[self.sura.pk])}?begin=1&end=2",
        )

    def test_memorization_can_start_at_ayat_zero(self):
        zero_ayat = Aiyat.objects.create(
            s_id=self.sura,
            number=0,
            text="بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
            audio_aiyat_end=1500,
        )

        response = self.client.get(
            reverse("memorize_sura", args=[self.sura.pk]),
            {"begin": 0, "end": 1},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, zero_ayat.text)
        self.assertContains(response, "Бисмилляхи")
        self.assertContains(response, "Аяты 0–1")
        self.assertContains(response, 'data-clip-start-ms="0"')
        self.assertContains(response, 'data-clip-end-ms="4200"')

    def test_only_the_start_ayat_field_accepts_zero(self):
        response = self.client.get(
            reverse("memorize_sura", args=[self.sura.pk]),
            {"begin": 0, "end": 0},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["range_selected"])
        self.assertIn("end", response.context["form"].errors)

    def test_memorization_rejects_reversed_ayat_range(self):
        response = self.client.get(
            reverse("memorize_sura", args=[self.sura.pk]),
            {"begin": 2, "end": 1},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Начальный аят не может быть больше конечного.")

    def test_memorization_rejects_a_range_with_unknown_ayat_numbers(self):
        response = self.client.get(
            reverse("memorize_sura", args=[self.sura.pk]),
            {"begin": 1, "end": 7},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "не найдены аяты с указанными номерами")

    def test_selected_range_without_timestamps_keeps_full_surah_player_visible(self):
        Aiyat.objects.create(s_id=self.sura, number=2, text="Аят без аудиометок")

        response = self.client.get(
            reverse("memorize_sura", args=[self.sura.pk]),
            {"begin": 2, "end": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Плеер не будет воспроизводить всю суру")
        self.assertContains(response, '<div class="player-panel">')
        self.assertContains(response, 'src="/media/audio/001.mp3"')
        self.assertContains(response, 'data-clip-required="true"')
        self.assertNotContains(response, "Слушать выбранный фрагмент")

    def test_audio_without_selected_range_plays_the_full_surah(self):
        response = self.client.get(reverse("memorize_sura", args=[self.sura.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Аудиочтение Аль-Фатиха")
        self.assertContains(response, 'src="/media/audio/001.mp3"')
        self.assertNotContains(response, "data-clip-start-ms=")
        self.assertNotContains(response, "data-clip-required=")

    def test_reading_page_redirects_to_memorization(self):
        response = self.client.get(reverse("detail", args=[self.sura.pk]))

        self.assertRedirects(response, reverse("memorize_sura", args=[self.sura.pk]))

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
