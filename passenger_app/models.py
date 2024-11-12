from django.db import models

from agent_management_app.models import AgentInfo
from visa_management_app.models import Visa
# Create your models here.


class Passenger(models.Model):
    gender_fields = (("male", "Male"), ("female", "Female"))

    # passport
    passport = models.CharField(max_length=50, blank=True, null=True, unique=True)
    passport_date_of_expairy = models.DateField(blank=True, null=True)

    # Relationship with Middleman Model.
    agent_list = models.ForeignKey(
        AgentInfo,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="passenger_agent",
    )

    # passenger information
    full_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=30, choices=gender_fields, blank=True, null=True
    )

    birth_date = models.DateField(("Birth date"), blank=True, null=True)
    email = models.EmailField(("Email"), max_length=254, blank=True, null=True)
    phone_number = models.CharField(
        ("Phone number"), blank=True, null=True, max_length=50, unique=True
    )
    address = models.TextField(
        ("Address"),
        max_length=254,
        blank=True,
        null=True,
    )
    emergency_contact_number = models.CharField(
        ("emergency contact number"), blank=True, null=True, max_length=50
    )
    passenger_image = models.ImageField(
        upload_to="passenger/passenger_images/", blank=True, null=True
    )

    # passenger manage
    fly_status = models.BooleanField(default=False, blank=True, null=True)
    cancel_status = models.BooleanField(default=False, blank=True, null=True)

    money_refund_status = models.BooleanField(default=False, blank=True, null=True)
    status = models.BooleanField(default=True, blank=True, null=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.full_name


##not needed
class PassengerPassport(models.Model):
    passenger_passport = models.ForeignKey(
        Passenger,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="passport_info_passenger",
    )
    passport_number = models.CharField(max_length=50, blank=True, null=True)
    date_of_expairy = models.DateField(blank=True, null=True)

    # passport image
    passport_scanned_image = models.FileField(
        upload_to="passenger/passenger_passport_images/", blank=True, null=True
    )

    # passport tracking
    passport_received = models.BooleanField(default=False, blank=True, null=True)
    police_clearance = models.BooleanField(default=False, blank=True, null=True)
    medical_certificate = models.BooleanField(default=False, blank=True, null=True)
    mofa_status = models.BooleanField(default=False, blank=True, null=True)
    finger_appointment = models.BooleanField(default=False, blank=True, null=True)
    visa_status = models.BooleanField(default=False, blank=True, null=True)
    training_status = models.BooleanField(default=False, blank=True, null=True)
    finger_status = models.BooleanField(default=False, blank=True, null=True)
    manpower_status = models.BooleanField(default=False, blank=True, null=True)
    ticket_status = models.BooleanField(default=False, blank=True, null=True)

    last_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)


# Passenger Transaction Account.
class PassengerTransaction(models.Model):
    passenger = models.ForeignKey(
        Passenger,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="passenger_account",
    )

    total_balance = models.FloatField(default=0.0, blank=True, null=True)
    credit = models.FloatField(default=0.0, blank=True, null=True)
    debit = models.FloatField(default=0.0, blank=True, null=True)
    note = models.TextField(null=True, blank=True)

    # Transaction Number.
    payment_transaction_id = models.CharField(
        max_length=20, blank=True, null=True
    )  # Auto Create.

    date = models.DateField(auto_now_add=True)

    transaction_date = models.DateField(blank=True, null=True)


class PassengerDocument(models.Model):
    TYPE_CHOICES = [
        ("pdf", "Pdf"),
        ("image", "Image"),
        ("word", "Word"),
    ]

    DOCUMENT_NAME_CHOICES = [
        ("passport_received", "Passport Received Status"),
        ("police_clearance", "Police Clearance Status"),
        ("medical_certificate", "Medical Certificate Status"),
        ("mofa_status", "MOFA Status"),
        ("finger_appointment", "Finger Appointment Status"),
        ("visa_status", "Visa Status"),
        ("training_status", "Training Status"),
        ("finger_status", "Finger Status"),
        ("manpower_status", "Manpower Status"),
        ("ticket_status", "Ticket Status"),
        ("flight", "Flight Status"),
    ]

    passenger = models.ForeignKey(
        Passenger,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="passenger_document",
    )
    visa = models.ForeignKey(
        Visa, blank=True, null=True, on_delete=models.CASCADE, related_name="visa"
    )

    document_name = models.CharField(
        max_length=50, blank=True, null=True, choices=DOCUMENT_NAME_CHOICES
    )  # WILL Be choices option as like PassengerPassport option tracking.
    document_type = models.CharField(
        max_length=20, null=True, blank=True, choices=TYPE_CHOICES, default="pdf"
    )
    document_file = models.FileField(
        upload_to="passenger/passenger_documents/", blank=True, null=True
    )
    note = models.CharField(max_length=255, blank=True, null=True)  #
    description = models.TextField(null=True, blank=True)
    visa = models.ForeignKey(
        Visa, blank=True, null=True, on_delete=models.CASCADE, related_name="visa"
    )

    collected_data = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    expiry_days = models.IntegerField(blank=True, null=True, default=0)
    status = models.BooleanField(blank=True, null=True, default=True)  #
    creation_date = models.DateField(auto_now_add=True, null=True, blank=True)
    flight_date = models.DateField(null=True, blank=True)
    # fly_status=models.BooleanField(default=False)


class PassengerGeneralDocument(models.Model):
    TYPE_CHOICES = [
        ("pdf", "Pdf"),
        ("image", "Image"),
        ("word", "Word"),
    ]

    passenger = models.ForeignKey(
        Passenger,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="passenger_general_document",
    )

    document_name = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(
        max_length=20, null=True, blank=True, choices=TYPE_CHOICES, default="pdf"
    )
    document_file = models.FileField(
        upload_to="passenger/passenger_general_documents/", blank=True, null=True
    )
    note = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    expiry_date = models.DateField(null=True, blank=True)

    creation_date = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.document_name
