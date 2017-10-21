from django import forms
from .models import Lecture


class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ("title", "day_of_week", "period")
        widgets = {
            "title": forms.TextInput(attrs={'class': 'form-control'}),
            "day_of_week": forms.Select(attrs={'class': 'form-control'}),
            "period": forms.Select(attrs={'class': 'form-control'})
        }
