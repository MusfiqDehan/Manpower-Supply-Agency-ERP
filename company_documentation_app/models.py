from django.db import models


class CompanyDocumentCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CompanyDocument(models.Model):
    # Documentation Type
    DOCUMENT_TYPES = (
        ("license", "Business License"),
        ("insurance", "Insurance"),
        ("permits", "Permits"),
        ("contracts", "Contracts"),
        ("financial_statements", "Financial Statements"),
        ("others", "Others"),
    )

    # Fields for the CompanyDocument model
    document_type = models.CharField(
        max_length=100, blank=True, null=True, choices=DOCUMENT_TYPES
    )
    document_category = models.ForeignKey(
        CompanyDocumentCategory,
        on_delete=models.SET_NULL,
        related_name="company_document",
        blank=True,
        null=True,
    )
    document_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    document_number = models.CharField(max_length=50, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    document_file = models.FileField(
        upload_to="company_general_documents/",
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True, default=True)
    upload_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.document_name
