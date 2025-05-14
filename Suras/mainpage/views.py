from django.shortcuts import render
from django.views.decorators.cache import cache_page
from pydub import AudioSegment
import base64
from .models import *
from .forms import *

def index(request):
    Suras = Sura.objects.all()
    context = {'Suras': Suras}
    return render(request, 'mainpage/index.html', context)

# @cache_page(60 * 15)
def detail(request, Sura_id):
    Suras = Sura.objects.get(pk=Sura_id)
    Ayats = Aiyat.objects.filter(s_id=Suras)
    context = {'Ayats': Ayats, 'Sura': Suras}
    return render(request, 'mainpage/detail.html', context)

def experiment(request):
    if request.method == 'POST':
        form = AiyatForm(request.POST)
        if form.is_valid():
            ayat_number = form.cleaned_data['number']
            sura_number = form.cleaned_data['s_id']
            Ayats = Aiyat.objects.get(number=ayat_number, s_id=sura_number)
            # form.save()
            context = {'form': form, 'Ayats': Ayats}
            return render(request, 'mainpage/experiment.html', context)
    else:
        form = AiyatForm()
        context = {'form': form}
        return render(request, 'mainpage/experiment.html', context)


