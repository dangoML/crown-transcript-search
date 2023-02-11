from django import forms
from .models import Witness

class WitnessForm(forms.ModelForm):
    class Meta:
        model = Witness
        fields = ['full_name','profile_picture']