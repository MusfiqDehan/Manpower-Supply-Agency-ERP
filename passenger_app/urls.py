from django.urls import path
from passenger_app.views import (
    passenger,
    passenger_details,
    passenger_document,
    passenger_general_document,
    passenger_passport,
    passport_tracking,
    passenger_search,
    all_passport,
    passport_report,
)


from passenger_app.views import fly_passenger, cancel_passenger


app_name = "passenger_app"
urlpatterns = [
    # Passenger_management
    path("passenger_view/", passenger.passenger_view, name="passenger"),
    path(
        "passenger/search/", passenger_search.passenger_search, name="passenger_search"
    ),
    path("passenger/create/", passenger.passenger_create, name="passenger_create"),
    path("passenger/<pk>/edit/", passenger.passenger_edit, name="passenger_edit"),
    path("passenger/<pk>/delete/", passenger.passenger_delete, name="passenger_delete"),
    # passenger details
    path(
        "passenger_details/<pk>/",
        passenger_details.passenger_details,
        name="passenger_details",
    ),
    path(
        "image/add/<passenger_id>/",
        passenger_passport.passport_image_add,
        name="passport_image_add",
    ),  # Not Working yet.
    # Successful/fly Passenger Management
    path("fly/", fly_passenger.fly_passengers, name="fly_passengers"),
    path("cancel/", cancel_passenger.cancel_passengers, name="cancel_passengers"),
    # Passenger Document
    path(
        "document/add/<passenger_id>/",
        passenger_document.passenger_document_add,
        name="passenger_document_add",
    ),
    path(
        "document/<pk>/edit/",
        passenger_document.passenger_document_edit,
        name="passenger_document_edit",
    ),
    path(
        "document/<pk>/delete/",
        passenger_document.passenger_document_delete,
        name="passenger_document_delete",
    ),
    # Passenger General Document CRUD URLs
    path(
        "passenger-general-document/<int:pk>/create/",
        passenger_general_document.document_create,
        name="passenger_general_document_create",
    ),
    path(
        "passenger-general-document/<int:pk>/edit/",
        passenger_general_document.document_edit,
        name="passenger_general_document_edit",
    ),
    path(
        "passenger-general-document/<int:pk>/delete/",
        passenger_general_document.document_delete,
        name="passenger_general_document_delete",
    ),
    # Passenger Account
    path(
        "account/create/<passenger_id>/",
        passenger_details.account_create,
        name="account_create",
    ),
    path("receive/<passenger_id>/", passenger_details.receive, name="receive"),
    path("payment/<passenger_id>/", passenger_details.payment, name="payment"),
    path(
        "account/<pk>/delete/", passenger_details.account_delete, name="account_delete"
    ),
    # passport tracking
    path(
        "passport/edit/<passenger_id>/",
        passport_tracking.passport_edit,
        name="passport_edit",
    ),
    path(
        "passport/tracking/update/<passenger_id>/",
        passport_tracking.passport_tracking_update,
        name="passport_tracking_update",
    ),
    # all passport
    path("all_passport/", all_passport.all_passport, name="all_passport"),
    path("passport/search/", all_passport.search_passport, name="search_passport"),
    # ====== Passport Report Management======
    path(
        "passport-received/",
        passport_report.passport_received,
        name="passport_received",
    ),
    path(
        "police-clearance/", passport_report.police_clearance, name="police_clearance"
    ),
    path(
        "medical-certificate/",
        passport_report.medical_certificate,
        name="medical_certificate",
    ),
    path("mofa-status/", passport_report.mofa_status, name="mofa_status"),
    path(
        "finger-appointment/",
        passport_report.finger_appointment,
        name="finger_appointment",
    ),
    path("visa-status/", passport_report.visa_status, name="visa_status"),
    path("training-status/", passport_report.training_status, name="training_status"),
    path("finger-status/", passport_report.finger_status, name="finger_status"),
    path("manpower-status/", passport_report.manpower_status, name="manpower_status"),
    path("ticket-status/", passport_report.ticket_status, name="ticket_status"),
    path("fly-success/", passport_report.fly_success, name="fly_success"),
]
