import pytest
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from ..models import AgentInfo, AgentDocument, AgentAccount, AgentTransaction


@pytest.mark.django_db
def test_create_edit_delete_agent_info():
    # Create
    agent = AgentInfo.objects.create(
        full_name="John Doe",
        gender="male",
        agent_id="A123",
        national_id="N123",
        visa_rate=100,
        email="john.doe@example.com",
        phone_number="1234567890",
        emergency_contact_number="0987654321",
        note="Test note",
        address="123 Test St",
        status=True,
    )
    assert AgentInfo.objects.count() == 1

    # Edit
    agent.full_name = "Jane Doe"
    agent.save()
    agent.refresh_from_db()
    assert agent.full_name == "Jane Doe"

    # Delete
    agent.delete()
    assert AgentInfo.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_agent_document():
    agent = AgentInfo.objects.create(full_name="John Doe")

    # Create
    document = AgentDocument.objects.create(
        agent=agent,
        document_name="Passport",
        document_type="pdf",
        document_description="Test description",
        collected_data="2023-01-01",
        expiry_date="2024-01-01",
        expiry_days=365,
        document_statu=True,
    )
    assert AgentDocument.objects.count() == 1

    # Edit
    document.document_name = "Visa"
    document.save()
    document.refresh_from_db()
    assert document.document_name == "Visa"

    # Delete
    document.delete()
    assert AgentDocument.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_agent_account():
    agent = AgentInfo.objects.create(full_name="John Doe")

    # Create
    account = AgentAccount.objects.create(
        agent=agent,
        agent_payable=1000.0,
        agent_total_credit=500.0,
        agent_total_debit=200.0,
        opening_balance=300.0,
        previous_balance=100.0,
        total_balance=400.0,
        is_credit=True,
        note="Test account note",
        account_status=True,
    )
    assert AgentAccount.objects.count() == 1

    # Edit
    account.agent_payable = 2000.0
    account.save()
    account.refresh_from_db()
    assert account.agent_payable == 2000.0

    # Delete
    account.delete()
    assert AgentAccount.objects.count() == 0


@pytest.mark.django_db
def test_create_edit_delete_agent_transaction():
    agent = AgentInfo.objects.create(full_name="John Doe")
    account = AgentAccount.objects.create(agent=agent)

    # Create
    transaction = AgentTransaction.objects.create(
        agent_account=account,
        payment_type="Cash",
        note="Test transaction note",
        online_transaction_number="ON123",
        bank_transaction_number="BN123",
        balance=100.0,
        credit=50.0,
        debit=20.0,
        transaction_hold_status=False,
        payment_transaction_id="PT123",
        payment_date="2023-01-01",
        payment_status=True,
    )
    assert AgentTransaction.objects.count() == 1

    # Edit
    transaction.payment_type = "Bank"
    transaction.save()
    transaction.refresh_from_db()
    assert transaction.payment_type == "Bank"

    # Delete
    transaction.delete()
    assert AgentTransaction.objects.count() == 0
