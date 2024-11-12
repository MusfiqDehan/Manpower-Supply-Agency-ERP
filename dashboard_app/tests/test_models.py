import pytest
from datetime import date
from agent_management_app.models import AgentInfo
from passenger_app.models import Passenger
from ..models import Notification


@pytest.mark.django_db
def test_create_edit_delete_notification():
    # Create related objects
    agent = AgentInfo.objects.create(full_name="Agent John Doe")
    passenger = Passenger.objects.create(full_name="Passenger Jane Doe")

    # Create
    notification = Notification.objects.create(
        name="Test Notification",
        description="This is a test notification",
        agent=agent,
        passenger=passenger,
        is_read=False,
        expiry_date=date(2023, 12, 31),  # Pass as a date object
    )
    assert Notification.objects.count() == 1
    assert notification.name == "Test Notification"
    assert notification.description == "This is a test notification"
    assert notification.agent == agent
    assert notification.passenger == passenger
    assert notification.is_read is False
    assert notification.expiry_date == date(2023, 12, 31)

    # Edit
    notification.name = "Updated Notification"
    notification.is_read = True
    notification.save()
    notification.refresh_from_db()
    assert notification.name == "Updated Notification"
    assert notification.is_read is True

    # Delete
    notification.delete()
    assert Notification.objects.count() == 0
