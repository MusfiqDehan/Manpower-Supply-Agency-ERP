import pytest
from datetime import date
from ..models import CostCategory, CompanyCost


@pytest.mark.django_db
def test_create_edit_delete_cost_category():
    # Create
    cost_category = CostCategory.objects.create(name="Category1")
    assert CostCategory.objects.count() == 1
    assert cost_category.name == "Category1"

    # Edit
    cost_category.name = "Category2"
    cost_category.save()
    cost_category.refresh_from_db()
    assert cost_category.name == "Category2"

    # Delete
    cost_category.delete()
    assert CostCategory.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_company_cost():
    cost_category = CostCategory.objects.create(name="Category1")

    # Create
    company_cost = CompanyCost.objects.create(
        date_incurred=date(2023, 1, 1),  # Convert string to date object
        category=cost_category,
        amount=1000,
        note="Test note",
    )
    assert CompanyCost.objects.count() == 1
    assert company_cost.date_incurred.strftime("%Y-%m-%d") == "2023-01-01"
    assert company_cost.category == cost_category
    assert company_cost.amount == 1000
    assert company_cost.note == "Test note"

    # Edit
    company_cost.amount = 2000
    company_cost.save()
    company_cost.refresh_from_db()
    assert company_cost.amount == 2000

    # Delete
    company_cost.delete()
    assert CompanyCost.objects.count() == 0
