from django.forms import ModelForm
from .models import *

class AiyatForm(ModelForm):
    class Meta:
        model = Aiyat
        fields = ('s_id', 'number')

class CheckedForm(ModelForm):
    class Meta:
        model = Aiyat
        fields = ('learn',)