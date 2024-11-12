from django.db import models


# Create your models here.
class AgentInfo(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    full_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, default="male", blank=True
    )

    agent_id = models.CharField(max_length=50, blank=True, null=True)

    national_id = models.CharField(max_length=50, blank=True, null=True)
    visa_rate = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)

    note = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(max_length=254, blank=True, null=True)
    image = models.ImageField(upload_to="agent/agent_images/", blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.full_name


# Agent Documentation model.
class AgentDocument(models.Model):
    TYPE_CHOICES = (
        ("pdf", "Pdf"),
        ("image", "Image"),
        ("word", "Word"),
    )

    # Relationship with Agent
    agent = models.ForeignKey(
        AgentInfo,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="agent_document",
    )

    document_name = models.CharField(max_length=256, blank=True, null=True)
    document_type = models.CharField(
        max_length=20, null=True, blank=True, choices=TYPE_CHOICES
    )
    document_file = models.FileField(
        upload_to="agent/agent_documents/", blank=True, null=True
    )
    document_description = models.TextField(null=True, blank=True)

    collected_data = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    expiry_days = models.IntegerField(blank=True, null=True, default=0)
    document_statu = models.BooleanField(null=True, blank=True, default=True)

    creation_date = models.DateField(auto_now_add=True, null=True, blank=True)


class AgentAccount(models.Model):
    # Agent Relationship
    agent = models.OneToOneField(
        AgentInfo,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="agent_account",
    )

    # all Passengers total amount(by agent visa rate) for each under passengers.
    agent_payable = models.FloatField(blank=True, null=True, default=0.0)
    agent_total_credit = models.FloatField(blank=True, null=True, default=0.0)
    agent_total_debit = models.FloatField(blank=True, null=True, default=0.0)

    opening_balance = models.FloatField(blank=True, null=True, default=0.0)
    previous_balance = models.FloatField(blank=True, null=True, default=0.0)
    total_balance = models.FloatField(blank=True, null=True, default=0.0)

    is_credit = models.BooleanField(blank=True, null=True, default=True)
    note = models.TextField(null=True, blank=True)
    account_status = models.BooleanField(default=True, blank=True, null=True)
    open_date = models.DateField(auto_now_add=True, blank=True, null=True)


class AgentTransaction(models.Model):
    # Payment Type Choices
    PAYMENT_TYPE_CHOICES = (
        ("Cash", "Cash Payment"),
        ("Bank", "Bank Transfer"),
        ("Online", "Online Payment"),
    )

    # AgentAccount Relationship
    agent_account = models.ForeignKey(
        AgentAccount,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="agent_account",
    )

    # Basic Payment Information
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES,
        blank=True,
        null=True,
        default="Cash",
    )  # Payment Type
    # For Cash Payment
    note = models.CharField(max_length=100, blank=True, null=True)
    # For Online
    online_transaction_number = models.CharField(max_length=50, blank=True, null=True)
    online_transaction_file = models.FileField(
        upload_to="agent/agent_transactions/agent_online_transaction_files/",
        blank=True,
        null=True,
    )
    # For Bank Payment
    bank_transaction_number = models.CharField(max_length=50, blank=True, null=True)
    bank_transaction_file = models.FileField(
        upload_to="agent/agent_transactions/agent_bank_transaction_files/",
        blank=True,
        null=True,
    )

    # Balance
    balance = models.FloatField(blank=True, null=True, default=0.0)
    credit = models.FloatField(blank=True, null=True, default=0.0)
    debit = models.FloatField(blank=True, null=True, default=0.0)

    # Agent Transaction will be hold when. not assign any passenger.
    transaction_hold_status = models.BooleanField(blank=True, null=True, default=False)

    # Transaction Number.
    payment_transaction_id = models.CharField(
        max_length=20, unique=True, blank=True, null=True
    )  # Auto Create.
    payment_date = models.DateField(blank=True, null=True)
    payment_status = models.BooleanField(blank=True, null=True, default=True)

    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
