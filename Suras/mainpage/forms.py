from django import forms
from django.forms import ModelForm

from .models import Aiyat


class AyatRangeForm(forms.Form):
    begin = forms.IntegerField(
        label="С аята",
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "0 или 1"}),
    )
    end = forms.IntegerField(
        label="По аят",
        min_value=1,
        widget=forms.NumberInput(attrs={"placeholder": "Например, 7"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        begin = cleaned_data.get("begin")
        end = cleaned_data.get("end")
        if begin is not None and end is not None and begin > end:
            raise forms.ValidationError("Начальный аят не может быть больше конечного.")
        return cleaned_data


class AiyatForm(ModelForm):
    class Meta:
        model = Aiyat
        fields = ('s_id', 'number')