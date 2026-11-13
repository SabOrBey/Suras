from django.db.models import Count
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import urlencode

from .forms import AiyatForm, AyatRangeForm
from .models import Aiyat, Dua, Hadith, Sura


def _session_ids(request, key):
    return {
        int(value)
        for value in request.session.get(key, [])
        if str(value).isdigit()
    }


def index(request):
    return render(request, "mainpage/index.html")


def detail(request, sura_id):
    get_object_or_404(Sura, pk=sura_id)
    return redirect("memorize_sura", sura_id=sura_id)


def memorization_index(request):
    suras = list(Sura.objects.annotate(ayat_count=Count("aiyat")).order_by("pk"))
    memorized_ids = _session_ids(request, "memorized_ayats")
    progress_by_sura = dict(
        Aiyat.objects.filter(pk__in=memorized_ids)
        .values("s_id_id")
        .annotate(count=Count("pk"))
        .values_list("s_id_id", "count")
    )
    for sura in suras:
        sura.memorized_count = progress_by_sura.get(sura.pk, 0)
    return render(
        request,
        "mainpage/memorization_index.html",
        {
            "Suras": suras,
            "memorized_count": sum(sura.memorized_count for sura in suras),
        },
    )


def memorize_sura(request, sura_id):
    sura = get_object_or_404(Sura, pk=sura_id)
    all_ayats = Aiyat.objects.filter(s_id=sura).order_by("number", "pk")
    ayats = list(all_ayats)
    form = AyatRangeForm(request.GET or None)
    range_selected = False
    range_error = None
    range_audio_start = None
    range_audio_end = None

    if form.is_valid():
        begin = form.cleaned_data["begin"]
        end = form.cleaned_data["end"]
        start_ayat = all_ayats.filter(number=begin).first()
        end_ayat = all_ayats.filter(number=end).last()
        if start_ayat is None or end_ayat is None:
            form.add_error(None, "В этой суре не найдены аяты с указанными номерами.")
        else:
            range_selected = True
            ayats = list(all_ayats.filter(number__gte=begin, number__lte=end))
            audio_start = start_ayat.audio_aiyat_begin
            if begin == 0 and audio_start is None:
                audio_start = 0
            audio_end = end_ayat.audio_aiyat_end
            if (
                audio_start is None
                or audio_end is None
                or audio_end <= audio_start
            ):
                range_error = "Для выбранного диапазона не размечены границы аудиофрагмента."
            else:
                range_audio_start = audio_start
                range_audio_end = audio_end
    else:
        ayats = list(all_ayats)

    memorized_ids = _session_ids(request, "memorized_ayats")
    for ayat in ayats:
        ayat.is_memorized = ayat.pk in memorized_ids
    return render(
        request,
        "mainpage/memorization_detail.html",
        {
            "Sura": sura,
            "Ayats": ayats,
            "form": form,
            "range_selected": range_selected,
            "range_error": range_error,
            "range_audio_start": range_audio_start,
            "range_audio_end": range_audio_end,
            "memorized_count": sum(ayat.is_memorized for ayat in ayats),
        },
    )


def toggle_memorized_ayat(request, sura_id, ayat_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    sura = get_object_or_404(Sura, pk=sura_id)
    ayat = get_object_or_404(Aiyat, pk=ayat_id, s_id=sura)
    memorized_ids = _session_ids(request, "memorized_ayats")
    if ayat.pk in memorized_ids:
        memorized_ids.remove(ayat.pk)
    else:
        memorized_ids.add(ayat.pk)
    request.session["memorized_ayats"] = sorted(memorized_ids)
    response = redirect("memorize_sura", sura_id=sura.pk)
    range_form = AyatRangeForm(request.GET)
    if range_form.is_valid():
        response["Location"] += f"?{urlencode(range_form.cleaned_data)}"
    return response


def lesson_library(request, section):
    if section == "hadith":
        model, title, description = (
            Hadith,
            "Изучение хадисов",
            "Читайте арабский текст, транскрипцию и перевод. Отмечайте хадисы, которые уже запомнили.",
        )
        session_key = "learned_hadiths"
    elif section == "dua":
        model, title, description = (
            Dua,
            "Раздел дуа",
            "Собирайте и изучайте дуа: их произношение, перевод и ситуации, в которых их читают.",
        )
        session_key = "learned_duas"
    else:
        raise Http404

    lessons = list(model.objects.all())
    completed_ids = _session_ids(request, session_key)
    for lesson in lessons:
        lesson.is_learned = lesson.pk in completed_ids
    return render(
        request,
        "mainpage/lesson_library.html",
        {
            "lessons": lessons,
            "section": section,
            "section_title": title,
            "section_description": description,
            "learned_count": sum(lesson.is_learned for lesson in lessons),
        },
    )


def toggle_lesson_completion(request, section, lesson_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    lessons = {
        "hadith": (Hadith, "learned_hadiths"),
        "dua": (Dua, "learned_duas"),
    }
    if section not in lessons:
        raise Http404
    model, session_key = lessons[section]
    lesson = get_object_or_404(model, pk=lesson_id)
    completed_ids = _session_ids(request, session_key)
    if lesson.pk in completed_ids:
        completed_ids.remove(lesson.pk)
    else:
        completed_ids.add(lesson.pk)
    request.session[session_key] = sorted(completed_ids)
    return redirect(reverse("lesson_library", kwargs={"section": section}))


def experiment(request):
    form = AiyatForm(request.POST or None)
    ayat = None
    if request.method == "POST" and form.is_valid():
        ayat = get_object_or_404(
            Aiyat.objects.select_related("s_id"),
            number=form.cleaned_data["number"],
            s_id=form.cleaned_data["s_id"],
        )
    return render(request, "mainpage/experiment.html", {"form": form, "Ayats": ayat})
