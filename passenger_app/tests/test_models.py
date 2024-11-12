import pytest
from datetime import date
from agent_management_app.models import AgentInfo
from visa_management_app.models import Visa
from ..models import (
    Passenger,
    PassengerPassport,
    PassengerTransaction,
    PassengerDocument,
    PassengerGeneralDocument,
)


@pytest.mark.django_db
def test_create_edit_delete_passenger():
    agent = AgentInfo.objects.create(full_name="Agent John Doe")

    # Create
    passenger = Passenger.objects.create(
        passport="P123456",
        passport_date_of_expairy="2025-01-01",
        agent_list=agent,
        full_name="Passenger Jane Doe",
        gender="female",
        birth_date="1990-01-01",
        email="jane.doe@example.com",
        phone_number="1234567890",
        address="123 Test St",
        emergency_contact_number="0987654321",
        fly_status=False,
        cancel_status=False,
        money_refund_status=False,
        status=True,
    )
    assert Passenger.objects.count() == 1
    assert passenger.full_name == "Passenger Jane Doe"

    # Edit
    passenger.full_name = "Passenger Jane Smith"
    passenger.save()
    passenger.refresh_from_db()
    assert passenger.full_name == "Passenger Jane Smith"

    # Delete
    passenger.delete()
    assert Passenger.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_passenger_passport():
    passenger = Passenger.objects.create(full_name="Passenger Jane Doe")

    # Create
    passport = PassengerPassport.objects.create(
        passenger_passport=passenger,
        passport_number="P123456",
        date_of_expairy="2025-01-01",
        passport_received=True,
        police_clearance=True,
        medical_certificate=True,
        mofa_status=True,
        finger_appointment=True,
        visa_status=True,
        training_status=True,
        finger_status=True,
        manpower_status=True,
        ticket_status=True,
    )
    assert PassengerPassport.objects.count() == 1
    assert passport.passport_number == "P123456"

    # Edit
    passport.passport_number = "P654321"
    passport.save()
    passport.refresh_from_db()
    assert passport.passport_number == "P654321"

    # Delete
    passport.delete()
    assert PassengerPassport.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_passenger_transaction():
    passenger = Passenger.objects.create(full_name="Passenger Jane Doe")

    # Create
    transaction = PassengerTransaction.objects.create(
        passenger=passenger,
        total_balance=1000.0,
        credit=500.0,
        debit=200.0,
        note="Test transaction",
        payment_transaction_id="T123456",
        transaction_date="2023-01-01",
    )
    assert PassengerTransaction.objects.count() == 1
    assert transaction.total_balance == 1000.0

    # Edit
    transaction.total_balance = 2000.0
    transaction.save()
    transaction.refresh_from_db()
    assert transaction.total_balance == 2000.0

    # Delete
    transaction.delete()
    assert PassengerTransaction.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_passenger_document():
    passenger = Passenger.objects.create(full_name="Passenger Jane Doe")
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

    # Create
    document = PassengerDocument.objects.create(
        passenger=passenger,
        visa=visa,
        document_name="passport_received",
        document_type="pdf",
        document_file="path/to/file.pdf",
        note="Test document",
        description="Test description",
        collected_data=date(2023, 1, 1),  # Pass as date object
        expiry_date=date(2024, 1, 1),  # Pass as date object
        expiry_days=365,
        status=True,
        flight_date=date(2023, 12, 31),  # Pass as date object
    )
    assert PassengerDocument.objects.count() == 1
    assert document.document_name == "passport_received"

    # Edit
    document.document_name = "police_clearance"
    document.save()
    document.refresh_from_db()
    assert document.document_name == "police_clearance"

    # Delete
    document.delete()
    assert PassengerDocument.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_passenger_general_document():
    passenger = Passenger.objects.create(full_name="Passenger Jane Doe")

    # Create
    general_document = PassengerGeneralDocument.objects.create(
        passenger=passenger,
        document_name="General Document",
        document_type="pdf",
        document_file="path/to/file.pdf",
        note="Test general document",
        description="Test description",
        expiry_date="2024-01-01",
    )
    assert PassengerGeneralDocument.objects.count() == 1
    assert general_document.document_name == "General Document"

    # Edit
    general_document.document_name = "Updated General Document"
    general_document.save()
    general_document.refresh_from_db()
    assert general_document.document_name == "Updated General Document"

    # Delete
    general_document.delete()
    assert PassengerGeneralDocument.objects.count() == 0
