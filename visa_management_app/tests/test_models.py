import pytest
from datetime import date
from ..models import Visa


@pytest.mark.django_db
def test_create_edit_delete_visa():
    # Create
    visa = Visa.objects.create(
        name="Tourist Visa",
        visa_id="V123456",
        sponsor_id="S123456",
        number_of_visa=10,
        office="Office A",
        details="Details about the visa",
        collected_data=date(2023, 1, 1),  # Pass as date object
        expiry_date=date(2024, 1, 1),  # Pass as date object
        expiry_days=365,
        file="path/to/file.pdf",
        status=True,
        reference="Ref123456",
    )
    assert Visa.objects.count() == 1
    assert visa.name == "Tourist Visa"
    assert visa.visa_id == "V123456"
    assert visa.sponsor_id == "S123456"
    assert visa.number_of_visa == 10
    assert visa.office == "Office A"
    assert visa.details == "Details about the visa"
    assert visa.collected_data == date(2023, 1, 1)
    assert visa.expiry_date == date(2024, 1, 1)
    assert visa.expiry_days == 365
    assert visa.file == "path/to/file.pdf"
    assert visa.status is True
    assert visa.reference == "Ref123456"

    # Edit
    visa.name = "Business Visa"
    visa.number_of_visa = 20
    visa.save()
    visa.refresh_from_db()
    assert visa.name == "Business Visa"
    assert visa.number_of_visa == 20

    # Delete
    visa.delete()
    assert Visa.objects.count() == 0
