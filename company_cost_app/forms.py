from django import forms
from .models import CompanyCost,CostCategory

class CompanyCostForm(forms.ModelForm):
    class Meta:
        model=CompanyCost
        fields='__all__'

class CostCategoryForm(forms.ModelForm):
    class Meta:
        model=CostCategory
        fields='__all__'     