from django import forms
from .models import patient,result


class PatientForm(forms.ModelForm):
    class Meta:
        model=patient
        fields='__all__'

class ResultForm(forms.ModelForm):
    class Meta:
        model=result
        fields='__all__'        