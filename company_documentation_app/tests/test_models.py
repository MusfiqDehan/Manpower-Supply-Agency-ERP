import pytest
from datetime import date
from ..models import CompanyDocumentCategory, CompanyDocument


@pytest.mark.django_db
def test_create_edit_delete_company_document():
    category = CompanyDocumentCategory.objects.create(name="Category1")

    # Create
    document = CompanyDocument.objects.create(
        document_type="license",
        document_category=category,
        document_name="Business License",
        document_number="12345",
        expiration_date=date(2024, 1, 1),  # Pass as a date object
        description="Test description",
        status=True,
    )
    assert CompanyDocument.objects.count() == 1
    assert document.document_type == "license"
    assert document.document_category == category
    assert document.document_name == "Business License"
    assert document.document_number == "12345"
    assert document.expiration_date.strftime("%Y-%m-%d") == "2024-01-01"
    assert document.description == "Test description"
    assert document.status is True

    # Edit
    document.document_name = "Updated Business License"
    document.save()
    document.refresh_from_db()
    assert document.document_name == "Updated Business License"

    # Delete
    document.delete()
    assert CompanyDocument.objects.count() == 0
