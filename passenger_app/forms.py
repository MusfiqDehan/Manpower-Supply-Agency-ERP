from django import forms
from passenger_app.models import (
    Passenger,
    PassengerTransaction,
    PassengerDocument,
    PassengerGeneralDocument,
    PassengerPassport,
)


class PassengerInfoSubmitForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = "__all__"


class PassportSubmitForm(forms.ModelForm):
    class Meta:
        model = PassengerPassport
        fields = "__all__"


class AccountInfoSubmitForm(forms.ModelForm):
    class Meta:
        model = PassengerTransaction
        fields = "__all__"


class DocumentSubmitForm(forms.ModelForm):
    class Meta:
        model = PassengerDocument
        fields = "__all__"


class PassengerGeneralDocumentForm(forms.ModelForm):
    class Meta:
        model = PassengerGeneralDocument
        fields = "__all__"


class TrackingForm(forms.ModelForm):
    class Meta:
        model = PassengerPassport
        fields = [
            "passenger_passport",
            "passport_number",
            "date_of_expairy",
            "passport_received",
            "police_clearance",
            "medical_certificate",
            "training_status",
            "visa_status",
            "mofa_status",
            "finger_status",
            "manpower_status",
            "ticket_status",
            "finger_appointment",
        ]


class PassportEditForm(forms.ModelForm):
    class Meta:
        model = PassengerPassport
        fields = ["passenger_passport", "passport_number", "date_of_expairy"]


class PassportImageForm(forms.ModelForm):
    class Meta:
        model = PassengerPassport
        fields = ["passport_scanned_image"]
