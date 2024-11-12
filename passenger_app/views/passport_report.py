from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from passenger_app.models import Passenger, PassengerDocument


@login_required
def passport_received(request):
    context = {
        "page_name": "Passport Status",
        "passport_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        passport_received_lists = PassengerDocument.objects.filter(
            document_name="passport_received"
        ).order_by("-id")
        context = {
            "page_name": "Passport Status",
            "passport_status": "active",
            "passport_received_list": [
                document
                for document in passport_received_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/passport_received.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "passport_status_view":
                        passport_received_lists = PassengerDocument.objects.filter(
                            document_name="passport_received"
                        ).order_by("-id")
                        context = {
                            "page_name": "Passport Status",
                            "passport_status": "active",
                            "passport_received_list": [
                                document
                                for document in passport_received_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/passport_received.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def police_clearance(request):
    context = {
        "page_name": "Police Clearance Status",
        "police_clearance_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        police_clearance_lists = PassengerDocument.objects.filter(
            document_name="police_clearance"
        ).order_by("-id")
        context = {
            "page_name": "Police Clearance Status",
            "police_clearance_status": "active",
            "police_clearance_list": [
                document
                for document in police_clearance_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/police_clearance.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "police_clearance_status_view":
                        police_clearance_lists = PassengerDocument.objects.filter(
                            document_name="police_clearance"
                        ).order_by("-id")
                        context = {
                            "page_name": "Police Clearance Status",
                            "police_clearance_status": "active",
                            "police_clearance_list": [
                                document
                                for document in police_clearance_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/police_clearance.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def medical_certificate(request):
    context = {
        "page_name": "Medical Certificate Status",
        "medical_certificate_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        medical_certificate_lists = PassengerDocument.objects.filter(
            document_name="medical_certificate"
        ).order_by("-id")
        context = {
            "page_name": "Medical Certificate Status",
            "medical_certificate_status": "active",
            "medical_certificate_list": [
                document
                for document in medical_certificate_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/medical_certificate.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "medical_certificate_status_view":
                        medical_certificate_lists = PassengerDocument.objects.filter(
                            document_name="medical_certificate"
                        ).order_by("-id")
                        context = {
                            "page_name": "Medical Certificate Status",
                            "medical_certificate_status": "active",
                            "medical_certificate_list": [
                                document
                                for document in medical_certificate_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/medical_certificate.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def training_status(request):
    context = {
        "page_name": "Training Status",
        "training_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        training_status_lists = PassengerDocument.objects.filter(
            document_name="training_status"
        ).order_by("-id")
        context = {
            "page_name": "Training Status",
            "training_status": "active",
            "training_status_list": [
                document
                for document in training_status_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/training_status.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "training_status_view":
                        training_status_lists = PassengerDocument.objects.filter(
                            document_name="training_status"
                        ).order_by("-id")
                        context = {
                            "page_name": "Training Status",
                            "training_status": "active",
                            "training_status_list": [
                                document
                                for document in training_status_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/training_status.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def visa_status(request):
    context = {
        "page_name": "Visa Status",
        "visa_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        visa_status_lists = PassengerDocument.objects.filter(
            document_name="visa_status"
        ).order_by("-id")
        context = {
            "page_name": "Visa Status",
            "visa_status": "active",
            "visa_status_list": [
                document
                for document in visa_status_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/visa_status.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "visa_status_view":
                        visa_status_lists = PassengerDocument.objects.filter(
                            document_name="visa_status"
                        ).order_by("-id")
                        context = {
                            "page_name": "Visa Status",
                            "visa_status": "active",
                            "visa_status_list": [
                                document
                                for document in visa_status_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/visa_status.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def mofa_status(request):
    context = {
        "page_name": "Mofa Status",
        "mofa_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        mofa_status_lists = PassengerDocument.objects.filter(
            document_name="mofa_status"
        ).order_by("-id")
        context = {
            "page_name": "Mofa Status",
            "mofa_status": "active",
            "mofa_status_list": [
                document
                for document in mofa_status_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/mofa_status.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "mofa_status_view":
                        mofa_status_lists = PassengerDocument.objects.filter(
                            document_name="mofa_status"
                        ).order_by("-id")
                        context = {
                            "page_name": "Mofa Status",
                            "mofa_status": "active",
                            "mofa_status_list": [
                                document
                                for document in mofa_status_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/mofa_status.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def finger_appointment(request):
    context = {
        "page_name": "Finger Appointment Status",
        "finger_appointment_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        finger_appointment_lists = PassengerDocument.objects.filter(
            document_name="finger_appointment"
        ).order_by("-id")
        context = {
            "page_name": "Finger Appointment Status",
            "finger_appointment_status": "active",
            "finger_appointment_list": [
                document
                for document in finger_appointment_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/finger_appointment.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "finger_appointment_view":
                        finger_appointment_lists = PassengerDocument.objects.filter(
                            document_name="finger_appointment"
                        ).order_by("-id")
                        context = {
                            "page_name": "Finger Appointment Status",
                            "finger_appointment_status": "active",
                            "finger_appointment_list": [
                                document
                                for document in finger_appointment_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/finger_appointment.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def finger_status(request):
    context = {
        "page_name": "Finger Status",
        "finger_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        finger_status_lists = PassengerDocument.objects.filter(
            document_name="finger_status"
        ).order_by("-id")
        context = {
            "page_name": "Finger Status",
            "finger_status": "active",
            "finger_status_list": [
                document
                for document in finger_status_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/finger_status.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "finger_status_view":
                        finger_status_lists = PassengerDocument.objects.filter(
                            document_name="finger_status"
                        ).order_by("-id")
                        context = {
                            "page_name": "Finger Status",
                            "finger_status": "active",
                            "finger_status_list": [
                                document
                                for document in finger_status_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/finger_status.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def manpower_status(request):
    context = {
        "page_name": "Manpower Status",
        "manpower_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        manpower_status_lists = PassengerDocument.objects.filter(
            document_name="manpower_status"
        ).order_by("-id")
        context = {
            "page_name": "Manpower Status",
            "manpower_status": "active",
            "manpower_status_list": [
                document
                for document in manpower_status_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/manpower_status.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "manpower_status_view":
                        manpower_status_lists = PassengerDocument.objects.filter(
                            document_name="manpower_status"
                        ).order_by("-id")
                        context = {
                            "page_name": "Manpower Status",
                            "manpower_status": "active",
                            "manpower_status_list": [
                                document
                                for document in manpower_status_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/manpower_status.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def ticket_status(request):
    context = {
        "page_name": "Ticket Status",
        "ticket_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        ticket_status_lists = PassengerDocument.objects.filter(
            document_name="ticket_status"
        ).order_by("-id")
        context = {
            "page_name": "Ticket Status",
            "ticket_status": "active",
            "ticket_status_list": [
                document
                for document in ticket_status_lists
                if not document.passenger.fly_status
            ],
            "user": request.user,
        }
        return render(request, "passport_report/ticket_status.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "ticket_status_view":
                        ticket_status_lists = PassengerDocument.objects.filter(
                            document_name="ticket_status"
                        ).order_by("-id")
                        context = {
                            "page_name": "Ticket Status",
                            "ticket_status": "active",
                            "ticket_status_list": [
                                document
                                for document in ticket_status_lists
                                if not document.passenger.fly_status
                            ],
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/ticket_status.html", context
                        )

            return render(request, "errors/403.html", context)


@login_required
def fly_success(request):
    context = {
        "page_name": "Fly Success Status",
        "fly_status": "active",
    }
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        flight_lists = PassengerDocument.objects.filter(
            document_name="flight", passenger__fly_status=True
        ).order_by("-id")
        context = {
            "page_name": "Fly Success Status",
            "fly_status": "active",
            "fly_status_list": flight_lists,
            "user": request.user,
        }
        return render(request, "passport_report/fly_success.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "fly_success_status_view":
                        flight_lists = PassengerDocument.objects.filter(
                            document_name="flight", passenger__fly_status=True
                        ).order_by("-id")
                        context = {
                            "page_name": "Fly Success Status",
                            "fly_status": "active",
                            "fly_status_list": flight_lists,
                            "user": request.user,
                        }
                        return render(
                            request, "passport_report/fly_success.html", context
                        )

            return render(request, "errors/403.html", context)
