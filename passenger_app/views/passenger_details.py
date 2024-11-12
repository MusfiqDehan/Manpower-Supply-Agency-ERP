from django.shortcuts import get_object_or_404, render
from passenger_app.forms import PassengerInfoSubmitForm, AccountInfoSubmitForm
from passenger_app.models import (
    Passenger,
    PassengerTransaction,
    PassengerDocument,
    PassengerGeneralDocument,
    PassengerPassport,
)
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum


# Passenger Details.
@login_required
def passenger_details(request, pk):
    user_groups = request.user.Group_Users.all()

    passenger = get_object_or_404(Passenger, id=pk)

    passenger_general_document_list = PassengerGeneralDocument.objects.filter(
        passenger=passenger.id
    )

    print(passenger_general_document_list)

    # passenger account
    account_list = PassengerTransaction.objects.filter(passenger__id=pk).order_by(
        "date", "id"
    )

    l = list(account_list)

    for i in range(0, len(l)):
        if i == 0:
            obj = l[i]

            obj.total_balance = obj.credit - obj.debit

            obj.save()

        else:
            p_obj = l[i - 1]
            p_balance = p_obj.total_balance
            obj = l[i]

            obj.total_balance = p_balance + obj.credit - obj.debit
            obj.save()

    try:
        account_opening_value = PassengerTransaction.objects.filter(
            passenger__id=pk
        ).first()
        if account_opening_value is not None:
            account_list_exclude_first = PassengerTransaction.objects.filter(
                passenger__id=pk
            ).order_by("date", "id")
        else:
            account_list_exclude_first = None

    except PassengerTransaction.DoesNotExist:
        account_opening_value = None
        account_list_exclude_first = None

    passenger_passport = PassengerPassport.objects.filter(
        passenger_passport__id=pk
    ).first()
    DOCUMENT_NAME_CHOICES = PassengerDocument.DOCUMENT_NAME_CHOICES

    # passenger documents
    passenger_document_list = PassengerDocument.objects.filter(
        passenger__id=pk
    ).order_by("document_name")

    passport_received = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="passport_received")
        .last()
    )
    police_clearance = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="police_clearance")
        .last()
    )
    medical_certificate = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="medical_certificate")
        .last()
    )
    mofa_status = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="mofa_status")
        .last()
    )
    finger_appointment = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="finger_appointment")
        .last()
    )
    visa_status = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="visa_status")
        .last()
    )
    training_status = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="training_status")
        .last()
    )
    finger_status = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="finger_status")
        .last()
    )
    manpower_status = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="manpower_status")
        .last()
    )
    ticket_status = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="ticket_status")
        .last()
    )
    flight = (
        PassengerDocument.objects.filter(passenger__id=pk)
        .filter(document_name="flight")
        .last()
    )

    # Get- Passenger total balance, total debit, and total credit
    result = PassengerTransaction.objects.filter(passenger_id=pk).aggregate(
        # total_balance=Sum('total_balance'),
        total_debit=Sum("debit"),
        total_credit=Sum("credit"),
    )
    # Passenger results
    passenger_total_debit = result["total_debit"] or 0.0
    passenger_total_credit = result["total_credit"] or 0.0
    # passenger_total_balance = result['total_balance'] or 0.0
    passenger_total_balance = (
        passenger_total_credit - passenger_total_debit
    )  # Total balance

    context = {
        "page_name": "Passenger Details",
        "passenger_details_nav_link_status": "active",
        "passenger": passenger,
        "passenger_general_document_list": passenger_general_document_list,
        "account_list": account_list,
        "account_opening_value": account_opening_value,
        "account_list_exclude_first": account_list_exclude_first,
        "passenger_document_list": passenger_document_list,
        "passenger_id": passenger.id,
        "passenger_passport": passenger_passport,
        "user": request.user,
        "passenger_total_balance": passenger_total_balance,
        "passenger_total_debit": passenger_total_debit,
        "passenger_total_credit": passenger_total_credit,
        "passport_received": passport_received,
        "police_clearance": police_clearance,
        "medical_certificate": medical_certificate,
        "visa_status": visa_status,
        "finger_appointment": finger_appointment,
        "training_status": training_status,
        "mofa_status": mofa_status,
        "finger_status": finger_status,
        "manpower_status": manpower_status,
        "ticket_status": ticket_status,
        "flight": flight,
        "DOCUMENT_NAME_CHOICES": DOCUMENT_NAME_CHOICES,
    }

    if request.user.is_superuser:
        return render(
            request,
            "passenger_app_templates/passenger_details/passenger_details.html",
            context,
        )
    else:
        if user_groups is None:
            return render(request, "errors/403.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "passenger_profile_view":
                        return render(
                            request,
                            "passenger_app_templates/passenger_details/passenger_details.html",
                            context,
                        )
            return render(request, "errors/403.html")


#############################################################################################################################
########################################  Passenger Account section ###########################################################
##################################################################################################################################


def save_account_form(request, form, passenger_id, template_name):
    data = dict()
    if request.method == "POST":
        if form.is_valid():
            new_form = form.save(commit=False)
            try:
                statements_loop = PassengerTransaction.objects.filter(
                    passenger__id=passenger_id
                ).order_by("date", "id")

                # if statements_loop:
                l = list(statements_loop)
                for i in range(0, len(l)):
                    if i == 0:
                        obj = l[i]
                        obj.previous_balance = 0.00
                        obj.save()

                    else:
                        p_obj = l[i - 1]
                        p_balance = p_obj.total_balance
                        obj = l[i]
                        obj.previous_balance = p_balance
                        obj.save()

                account_opening_value_ob = PassengerTransaction.objects.filter(
                    passenger__id=passenger_id
                ).last()
                if account_opening_value_ob is not None:
                    debit = request.POST.get("debit")
                    credit = request.POST.get("credit")

                    if debit == "0.0":
                        new_form.total_balance = (
                            account_opening_value_ob.total_balance + float(credit)
                        )
                        new_form.save()
                        data["form_is_valid"] = True
                        # Retrieve account list excluding the first one
                        account_opening_value = PassengerTransaction.objects.filter(
                            passenger__id=passenger_id
                        ).first()
                        account_list_exclude_first = (
                            PassengerTransaction.objects.filter(
                                passenger__id=passenger_id
                            )
                            .exclude(id=account_opening_value.id)
                            .order_by("date", "id")
                        )

                        # Render various templates and store them in the data dictionary
                        data["html_account_list"] = render_to_string(
                            "passenger_app_templates/passenger_details/account_list.html",
                            {
                                "account_list_exclude_first": account_list_exclude_first,
                                "passenger_id": passenger_id,
                                "user": request.user,
                            },
                        )
                        data["html_opening_bal_date"] = render_to_string(
                            "passenger_app_templates/passenger_details/opening_balance_date.html",
                            {
                                "account_opening_value": account_opening_value,
                                "user": request.user,
                            },
                        )
                        data["html_opening_balance"] = render_to_string(
                            "passenger_app_templates/passenger_details/opening_balance.html",
                            {
                                "account_opening_value": account_opening_value,
                                "user": request.user,
                            },
                        )
                        data["html_account_button"] = render_to_string(
                            "passenger_app_templates/passenger_details/account_button.html",
                            {
                                "account_opening_value": account_opening_value,
                                "passenger_id": passenger_id,
                                "user": request.user,
                            },
                        )
                        return JsonResponse(data)

                    else:
                        new_form.total_balance = (
                            account_opening_value_ob.total_balance - float(debit)
                        )
                        new_form.save()
                        data["form_is_valid"] = True
                        # Retrieve account list excluding the first one
                        account_opening_value = PassengerTransaction.objects.filter(
                            passenger__id=passenger_id
                        ).first()
                        account_list_exclude_first = (
                            PassengerTransaction.objects.filter(
                                passenger__id=passenger_id
                            )
                            .exclude(id=account_opening_value.id)
                            .order_by("date", "id")
                        )

                        # Render various templates and store them in the data dictionary
                        data["html_account_list"] = render_to_string(
                            "passenger_app_templates/passenger_details/account_list.html",
                            {
                                "account_list_exclude_first": account_list_exclude_first,
                                "passenger_id": passenger_id,
                                "user": request.user,
                            },
                        )
                        data["html_opening_bal_date"] = render_to_string(
                            "passenger_app_templates/passenger_details/opening_balance_date.html",
                            {
                                "account_opening_value": account_opening_value,
                                "user": request.user,
                            },
                        )
                        data["html_opening_balance"] = render_to_string(
                            "passenger_app_templates/passenger_details/opening_balance.html",
                            {
                                "account_opening_value": account_opening_value,
                                "user": request.user,
                            },
                        )
                        data["html_account_button"] = render_to_string(
                            "passenger_app_templates/passenger_details/account_button.html",
                            {
                                "account_opening_value": account_opening_value,
                                "passenger_id": passenger_id,
                                "user": request.user,
                            },
                        )
                        return JsonResponse(data)

                else:
                    #  the case where account_opening_value_ob is None
                    opening_balance = request.POST.get("opening_balance")
                    new_form.total_balance = opening_balance

                    new_form.save()

                    data["form_is_valid"] = True

                    # Retrieve account list excluding the first one
                    account_opening_value = PassengerTransaction.objects.filter(
                        passenger__id=passenger_id
                    ).first()
                    account_list_exclude_first = (
                        PassengerTransaction.objects.filter(passenger__id=passenger_id)
                        .exclude(id=account_opening_value.id)
                        .order_by("date", "id")
                    )

                    # Render various templates and store them in the data dictionary
                    data["html_account_list"] = render_to_string(
                        "passenger_app_templates/passenger_details/account_list.html",
                        {
                            "account_list_exclude_first": account_list_exclude_first,
                            "passenger_id": passenger_id,
                            "user": request.user,
                        },
                    )
                    data["html_opening_bal_date"] = render_to_string(
                        "passenger_app_templates/passenger_details/opening_balance_date.html",
                        {
                            "account_opening_value": account_opening_value,
                            "user": request.user,
                        },
                    )
                    data["html_opening_balance"] = render_to_string(
                        "passenger_app_templates/passenger_details/opening_balance.html",
                        {
                            "account_opening_value": account_opening_value,
                            "user": request.user,
                        },
                    )
                    data["html_account_button"] = render_to_string(
                        "passenger_app_templates/passenger_details/account_button.html",
                        {
                            "account_opening_value": account_opening_value,
                            "passenger_id": passenger_id,
                            "user": request.user,
                        },
                    )
                    return JsonResponse(data)

            except Exception as e:
                # Handle exceptions that may occur when accessing attributes or performing calculations

                data["form_is_valid"] = False
                data["error_message"] = str(e)

            return JsonResponse(data)

    else:
        data["form_is_valid"] = False

    context = {
        "form": form,
        "passenger_id": passenger_id,
        "user": request.user,
    }

    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# account create for the first time transaction
@login_required
def account_create(request, passenger_id):
    if request.method == "POST":
        form = AccountInfoSubmitForm(request.POST)

    else:
        passenger_id = passenger_id
        form = AccountInfoSubmitForm()

    return save_account_form(
        request,
        form,
        passenger_id,
        "passenger_app_templates/passenger_details/create_account.html",
    )


#  Middle Man Transaction amount Receive  ( credited )
@login_required
def receive(request, passenger_id):
    if request.method == "POST":
        form = AccountInfoSubmitForm(request.POST)

    else:
        passenger_id = passenger_id
        form = AccountInfoSubmitForm()

    return save_account_form(
        request,
        form,
        passenger_id,
        "passenger_app_templates/passenger_details/receive.html",
    )


# amount payment ( debited)
@login_required
def payment(request, passenger_id):
    if request.method == "POST":
        form = AccountInfoSubmitForm(request.POST)

    else:
        passenger_id = passenger_id
        form = AccountInfoSubmitForm()

    return save_account_form(
        request,
        form,
        passenger_id,
        "passenger_app_templates/passenger_details/payment.html",
    )


# delete
def save_account_delete_form(request, account, template_name):
    data = dict()

    object = account
    passenger_op = account.passenger.id

    if request.method == "POST":
        object.delete()

        statements_loop = PassengerTransaction.objects.filter(
            passenger__id=passenger_op
        ).order_by("date", "id")

        # if statements_loop:
        l = list(statements_loop)
        for i in range(0, len(l)):
            if i == 0:
                obj = l[i]
                obj.previous_balance = 0.00
                obj.save()

            else:
                p_obj = l[i - 1]
                p_balance = p_obj.total_balance
                obj = l[i]
                obj.previous_balance = p_balance
                obj.total_balance = (
                    obj.previous_balance + obj.credit - obj.debit
                )  # total balance update when deleting a row
                obj.save()

        account_opening_value = PassengerTransaction.objects.filter(
            passenger__id=passenger_op
        ).last()

        data["form_is_valid"] = True

        # Retrieve account list excluding the first one
        account_opening_value = PassengerTransaction.objects.filter(
            passenger__id=passenger_op
        ).first()
        account_list_exclude_first = (
            PassengerTransaction.objects.filter(passenger__id=passenger_op)
            .exclude(id=account_opening_value.id)
            .order_by("date", "id")
        )

        # Render various templates and store them in the data dictionary
        data["html_account_list"] = render_to_string(
            "passenger_app_templates/passenger_details/account_list.html",
            {
                "account_list_exclude_first": account_list_exclude_first,
                "user": request.user,
            },
        )
        return JsonResponse(data)
    else:
        data["form_is_valid"] = False

    context = {
        "account": account,
        "user": request.user,
    }

    data["html_form"] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


# Account Delete
@login_required
def account_delete(request, pk):
    account = PassengerTransaction.objects.get(id=pk)

    return save_account_delete_form(
        request,
        account,
        "passenger_app_templates/passenger_details/delete_account.html",
    )
