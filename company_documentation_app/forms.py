from django import forms

from company_documentation_app.models import CompanyDocument, CompanyDocumentCategory


# Company Documentation
class CompanyDocumentForm(forms.ModelForm):
    class Meta:
        model = CompanyDocument
        fields = "__all__"


# Company Documentation Category
class CompanyDocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = CompanyDocumentCategory
        fields = "__all__"
