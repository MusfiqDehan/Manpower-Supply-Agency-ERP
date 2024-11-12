from django.shortcuts import render
from passenger_app.forms import (
    PassengerInfoSubmitForm,
    AccountInfoSubmitForm,
    DocumentSubmitForm,
)
from passenger_app.models import Passenger, PassengerTransaction, PassengerDocument
from visa_management_app.models import Visa
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404


# Passenger Documentation Add/create
@login_required
def passenger_document_add(request, passenger_id):
    passenger = get_object_or_404(
        Passenger, id=passenger_id
    )  # Assuming you have a Passenger model
    document = None  # You can specify a document object if needed, otherwise, it's None
    data = {}

    # choice field of document name--
    DOCUMENT_NAME_CHOICES = PassengerDocument.DOCUMENT_NAME_CHOICES
    passenger_documents = PassengerDocument.objects.filter(passenger__id=passenger_id)
    documents_submitted = []
    for document in passenger_documents:
        documents_submitted.append(document.document_name)

    visa_list = Visa.objects.filter(number_of_visa__gt=0)

    if request.method == "POST":
        visa_pk = request.POST.get("visa", None)

        form = DocumentSubmitForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.passenger = (
                passenger  # Assign the passenger to the form instance
            )
            form.save()

            # --------------visa--------------
            if visa_pk:
                visa = Visa.objects.get(pk=int(visa_pk))
                visa.number_of_visa -= 1
                visa.save()
            # --------------visa--------------

            if form.cleaned_data["document_name"] == "flight":
                passenger.fly_status = True
                passenger.save()
            print(passenger.fly_status, "fly_status")

            data["form_is_valid"] = True
            passenger_document_list = PassengerDocument.objects.filter(
                passenger=passenger
            ).order_by("document_name")
            data["html_passenger_document_list"] = render_to_string(
                "passenger_app_templates/passenger_details/documents/document_list.html",
                {
                    "passenger_document_list": passenger_document_list,
                    "user": request.user,
                },
            )

            passport_received = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="passport_received")
                .last()
            )
            police_clearance = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="police_clearance")
                .last()
            )
            medical_certificate = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="medical_certificate")
                .last()
            )
            mofa_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="mofa_status")
                .last()
            )
            finger_appointment = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="finger_appointment")
                .last()
            )
            visa_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="visa_status")
                .last()
            )
            training_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="training_status")
                .last()
            )
            finger_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="finger_status")
                .last()
            )
            manpower_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="manpower_status")
                .last()
            )
            ticket_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="ticket_status")
                .last()
            )
            flight = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="flight")
                .last()
            )
            ##passenger_documents=PassengerDocument.objects.filter(passenger__id= passenger_id)

            context = {
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
                "documents_submitted": documents_submitted,
                "visa_list": visa_list,
            }
            data["tracking_steps_html"] = render_to_string(
                "passenger_app_templates/passenger_details/passport/tracking_steps.html",
                context,
                request=request,
            )
        # data['passport_image_html']=render_to_string('passenger_app_templates/passenger_details/passport_image.html',context,request=request)
        else:
            data["form_is_valid"] = False
    else:
        form = DocumentSubmitForm()  # GET request

    context = {
        "form": form,
        "passenger_id": passenger_id,
        "document": document,
        "user": request.user,
        "DOCUMENT_NAME_CHOICES": DOCUMENT_NAME_CHOICES,
        "documents_submitted": documents_submitted,
        "visa_list": visa_list,
    }

    data["html_form"] = render_to_string(
        "passenger_app_templates/passenger_details/documents/add_document.html",
        context,
        request=request,
    )
    return JsonResponse(data)


def passenger_document_edit(request, pk):
    data = dict()

    document = PassengerDocument.objects.get(pk=pk)

    document_visa = None
    if document.visa:
        document_visa = document.visa.pk

    passenger_id = document.passenger.id
    passenger = Passenger.objects.get(id=passenger_id)

    visa_list = Visa.objects.filter(number_of_visa__gt=0)

    if request.method == "POST":
        visa_pk = request.POST.get("visa", None)

        form = DocumentSubmitForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            # --------------visa--------------
            if visa_pk and document_visa:
                if int(visa_pk) != document_visa:
                    visa = Visa.objects.get(pk=int(visa_pk))
                    visa.number_of_visa -= 1
                    visa.save()

                    document_visa = Visa.objects.get(pk=document_visa)
                    document_visa.number_of_visa += 1
                    document_visa.save()

            if visa_pk and not document_visa:
                visa = Visa.objects.get(pk=int(visa_pk))
                visa.number_of_visa -= 1
                visa.save()

            # --------------visa--------------

            form.save()

            if form.cleaned_data["document_name"] == "flight":
                passenger.fly_status = True
                passenger.save()
            else:
                passenger.fly_status = False
                passenger.save()
            data["form_is_valid"] = True

            passenger_document_list = PassengerDocument.objects.filter(
                passenger=passenger_id
            ).order_by("document_name")
            data["html_passenger_document_list"] = render_to_string(
                "passenger_app_templates/passenger_details/documents/document_list.html",
                {
                    "passenger_document_list": passenger_document_list,
                    "user": request.user,
                },
            )
            passport_received = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="passport_received")
                .last()
            )
            police_clearance = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="police_clearance")
                .last()
            )
            medical_certificate = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="medical_certificate")
                .last()
            )
            mofa_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="mofa_status")
                .last()
            )
            finger_appointment = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="finger_appointment")
                .last()
            )
            visa_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="visa_status")
                .last()
            )
            training_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="training_status")
                .last()
            )
            finger_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="finger_status")
                .last()
            )
            manpower_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="manpower_status")
                .last()
            )
            ticket_status = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="ticket_status")
                .last()
            )
            flight = (
                PassengerDocument.objects.filter(passenger__id=passenger_id)
                .filter(document_name="flight")
                .last()
            )
            context = {
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
                "visa_list": visa_list,
            }
            data["tracking_steps_html"] = render_to_string(
                "passenger_app_templates/passenger_details/passport/tracking_steps.html",
                context,
                request=request,
            )
            return JsonResponse(data)
        else:
            print(form.errors)
            data["form_is_valid"] = False
            form = DocumentSubmitForm(instance=document)
            form = DocumentSubmitForm(instance=document)
            context = dict(document=document, form=form)
            data["html_form"] = render_to_string(
                "passenger_app_templates/passenger_details/documents/edit_document.html",
                context,
                request=request,
            )
            return JsonResponse(data)
    else:
        form = DocumentSubmitForm(instance=document)
        context = dict(
            document=document,
            form=form,
            visa_list=visa_list,
        )
        data["html_form"] = render_to_string(
            "passenger_app_templates/passenger_details/documents/edit_document.html",
            context,
            request=request,
        )
        return JsonResponse(data)


# Passenger Documentation Delete
@login_required
def passenger_document_delete(request, pk):
    document = get_object_or_404(PassengerDocument, id=pk)

    # document=PassengerDocument.objects.get(id=pk)
    passenger_id = document.passenger.pk
    passenger = Passenger.objects.get(id=passenger_id)

    data = {}

    if request.method == "POST":
        if document.document_name == "flight":
            passenger.fly_status = False
            passenger.save()

        ##-------------visa---------------
        if document.document_name == "visa_status":
            visa = Visa.objects.get(pk=document.visa.pk)
            visa.number_of_visa += 1
            visa.save()
        ##--------------visa-----------------

        document.delete()
        data["form_is_valid"] = True
        passenger_document_list = PassengerDocument.objects.filter(
            passenger__id=passenger_id
        ).order_by("document_name")
        data["html_passenger_document_list"] = render_to_string(
            "passenger_app_templates/passenger_details/documents/document_list.html",
            {
                "passenger_document_list": passenger_document_list,
                "user": request.user,
            },
        )
        passport_received = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="passport_received")
            .last()
        )
        police_clearance = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="police_clearance")
            .last()
        )
        medical_certificate = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="medical_certificate")
            .last()
        )
        mofa_status = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="mofa_status")
            .last()
        )
        finger_appointment = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="finger_appointment")
            .last()
        )
        visa_status = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="visa_status")
            .last()
        )
        training_status = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="training_status")
            .last()
        )
        finger_status = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="finger_status")
            .last()
        )
        manpower_status = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="manpower_status")
            .last()
        )
        ticket_status = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="ticket_status")
            .last()
        )
        flight = (
            PassengerDocument.objects.filter(passenger__id=passenger_id)
            .filter(document_name="flight")
            .last()
        )
        context = {
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
        }

        data["tracking_steps_html"] = render_to_string(
            "passenger_app_templates/passenger_details/passport/tracking_steps.html",
            context,
            request=request,
        )
        # data['passport_image_html']=render_to_string('passenger_app_templates/passenger_details/passport_image.html',context,request=request)
    else:
        data["form_is_valid"] = False

    context = {
        "document": document,
        "user": request.user,
    }

    data["html_form"] = render_to_string(
        "passenger_app_templates/passenger_details/documents/delete_document.html",
        context,
        request=request,
    )
    return JsonResponse(data)


# Passenger Document Edit.
# @login_required
# def passenger_document_edit(request, pk):
# document = get_object_or_404(PassengerDocument, id=pk)  # Replace "PassengerDocument" with your actual model name
# passenger_id = document.passenger.id
# data = {}

# DOCUMENT_NAME_CHOICES=PassengerDocument.DOCUMENT_NAME_CHOICES
# passenger_documents=PassengerDocument.objects.filter(passenger__id= passenger_id)
# documents_submitted=[]
# for document in passenger_documents:

#             documents_submitted.append(document.document_name)


# if request.method == 'POST':
#     form = DocumentSubmitForm(request.POST, request.FILES, instance=document)

#     if form.is_valid():
#         form.save()
#         data['form_is_valid'] = True
#         passenger_document_list = PassengerDocument.objects.filter(passenger=passenger_id).order_by('document_name')
#         data['html_passenger_document_list'] = render_to_string('passenger_app_templates/passenger_details/documents/document_list.html', {
#             'passenger_document_list': passenger_document_list,
#             'user': request.user,
#         })
#         passport_received=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='passport_received').last()
#         police_clearance=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='police_clearance').last()
#         medical_certificate=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='medical_certificate').last()
#         mofa_status=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='mofa_status').last()
#         finger_appointment=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='finger_appointment').last()
#         visa_status=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='visa_status').last()
#         training_status=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='training_status').last()
#         finger_status=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='finger_status').last()
#         manpower_status=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='manpower_status').last()
#         ticket_status=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='ticket_status').last()
#         flight=PassengerDocument.objects.filter(passenger__id= passenger_id).filter(document_name='flight').last()
#         context={
#                 'passport_received': passport_received,
#                 'police_clearance':police_clearance,
#                 'medical_certificate': medical_certificate,
#                 'visa_status': visa_status,
#                 "finger_appointment": finger_appointment,
#                 'training_status': training_status,
#                 'mofa_status': mofa_status,
#                 'finger_status':finger_status,
#                 'manpower_status': manpower_status,
#                 'ticket_status':ticket_status,
#                 'flight':flight,
#         }
#         data['tracking_steps_html']=render_to_string('passenger_app_templates/passenger_details/passport/tracking_steps.html',context,request=request)
#         #data['passport_image_html']=render_to_string('passenger_app_templates/passenger_details/passport_image.html',context,request=request)
#     else:
#         data['form_is_valid'] = False
# else:
#     #form = DocumentSubmitForm(instance=document)

#     context = {

#         'passenger_id': passenger_id,
#         'document': document,
#         'user': request.user,
#         'DOCUMENT_NAME_CHOICES':DOCUMENT_NAME_CHOICES,
#         'documents_submitted':documents_submitted,
#     }

#     data['html_form'] = render_to_string('passenger_app_templates/passenger_details/documents/edit_document.html', context, request=request)
#     return JsonResponse(data)
