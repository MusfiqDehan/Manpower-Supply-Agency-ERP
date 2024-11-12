

from django import forms
from visa_management_app.models import Visa


# Visa Form
class VisaCreateForm(forms.ModelForm):
    class Meta:
        model = Visa
        fields='__all__'     
        