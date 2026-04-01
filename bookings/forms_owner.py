from django import forms
from .models import Table, OpeningHours

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ["identifier", "capacity"]


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = OpeningHours
        fields = ["day_of_week", "open_time", "close_time"]