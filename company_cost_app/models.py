from django.db import models


# Company Cost Category
class CostCategory(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Company Cost Model.
class CompanyCost(models.Model):
    date_incurred = models.DateField(blank=True, null=True)
    category = models.ForeignKey(
        CostCategory,
        on_delete=models.CASCADE,
        related_name="company_cost",
        blank=True,
        null=True,
    )
    amount = models.IntegerField(blank=True, null=True)
    cost_document = models.FileField(
        upload_to="company_cost_documents/", blank=True, null=True
    )
    note = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category.name
