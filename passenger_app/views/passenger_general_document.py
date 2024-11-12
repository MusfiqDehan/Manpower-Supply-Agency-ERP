from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from passenger_app.models import PassengerGeneralDocument, Passenger
from passenger_app.forms import PassengerGeneralDocumentForm


@login_required
def document_create(request, pk):
    data = {}
    passenger = get_object_or_404(Passenger, id=pk)
    type_choices = PassengerGeneralDocument.TYPE_CHOICES
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            form = PassengerGeneralDocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data["form_is_valid"] = True
                passenger_general_document_list = (
                    PassengerGeneralDocument.objects.filter(
                        passenger=passenger
                    ).order_by("-id")
                )
                context = {
                    "passenger_general_document_list": passenger_general_document_list,
                    "user": request.user,
                    "passenger": passenger,
                    "type_choices": type_choices,
                }
                data["passenger_general_document_list"] = render_to_string(
                    "passenger_app_templates/passenger_details/passenger_general_document/create_document_list.html",
                    context,
                )
                return JsonResponse(data)
            else:
                print(form.errors)
                data["form_is_valid"] = False
                return JsonResponse(data)
        else:
            form = PassengerGeneralDocumentForm()
            context = {
                "form": form,
                "user": request.user,
                "passenger": passenger,
                "type_choices": type_choices,
            }
            data["html_form"] = render_to_string(
                "passenger_app_templates/passenger_details/passenger_general_document/create_document.html",
                context,
            )
            data["passenger_general_document_list"] = render_to_string(
                "passenger_app_templates/passenger_details/passenger_general_document/create_document_list.html",
                context,
            )
            return JsonResponse(data)
    else:
        if user_groups is None:
            return render(request, "errors/403-contents.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_create":
                        if request.method == "POST":
                            form = PassengerGeneralDocumentForm(
                                request.POST, request.FILES
                            )
                            if form.is_valid():
                                form.save()
                                data["form_is_valid"] = True
                                passenger_general_document_list = (
                                    PassengerGeneralDocument.objects.all().order_by(
                                        "-id"
                                    )
                                )
                                context = {
                                    "passenger_general_document_list": passenger_general_document_list,
                                    "user": request.user,
                                    "passenger": passenger,
                                    "type_choices": type_choices,
                                }
                                data["passenger_general_document_list"] = (
                                    render_to_string(
                                        "passenger_app_templates/passenger_details/passenger_general_document/create_document_list.html",
                                        context,
                                    )
                                )
                                return JsonResponse(data)
                            else:
                                data["form_is_valid"] = False
                                return JsonResponse(data)
                        else:
                            form = PassengerGeneralDocumentForm()

                            context = {
                                "form": form,
                                "user": request.user,
                                "passenger": passenger,
                                "type_choices": type_choices,
                            }
                            data["html_form"] = render_to_string(
                                "passenger_app_templates/passenger_details/passenger_general_document/create_document.html",
                                context,
                            )
                            return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


def document_edit(request, pk):
    data = dict()

    user_groups = request.user.Group_Users.all()
    type_choices = PassengerGeneralDocument.TYPE_CHOICES

    general_document = get_object_or_404(PassengerGeneralDocument, id=pk)

    passenger_id = general_document.passenger.id
    passenger = Passenger.objects.get(id=passenger_id)

    if request.method == "POST":
        form = PassengerGeneralDocumentForm(
            request.POST, request.FILES, instance=general_document
        )
        if form.is_valid():
            form.save()

            data["form_is_valid"] = True
            passenger_general_document_list = PassengerGeneralDocument.objects.filter(
                passenger=passenger
            ).order_by("-id")
            context = {
                "general_document": general_document,
                "passenger_general_document_list": passenger_general_document_list,
                "user": request.user,
                "passenger": passenger,
                "type_choices": type_choices,
            }
            data["passenger_general_document_list"] = render_to_string(
                "passenger_app_templates/passenger_details/passenger_general_document/create_document_list.html",
                context,
            )
            return JsonResponse(data)

        else:
            print(form.errors)
            data["form_is_valid"] = False
            return JsonResponse(data)

    else:
        form = PassengerGeneralDocumentForm(instance=general_document)

        context = {
            "form": form,
            "passenger": passenger,
            "user": request.user,
            "general_document": general_document,
            "type_choices": type_choices,
        }

    if request.user.is_superuser:
        data["html_form"] = render_to_string(
            "passenger_app_templates/passenger_details/passenger_general_document/document_edit.html",
            context,
        )
        return JsonResponse(data)

    else:
        if user_groups is None:
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_update":
                        data["html_form"] = render_to_string(
                            "passenger_app_templates/passenger_details/passenger_general_document/document_edit.html",
                            context,
                        )
                        return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


#  Delete
@login_required
def document_delete(request, pk):
    data = {}
    user_groups = request.user.Group_Users.all()

    general_document = get_object_or_404(PassengerGeneralDocument, id=pk)

    passenger_id = general_document.passenger.id
    passenger = Passenger.objects.get(id=passenger_id)

    passenger_general_document_list = PassengerGeneralDocument.objects.filter(
        passenger=passenger
    ).order_by("-id")

    if request.method == "POST":
        general_document.delete()

        data["form_is_valid"] = True
        passenger_general_document_list = PassengerGeneralDocument.objects.filter(
            passenger=passenger
        ).order_by("-id")
        context = {
            "general_document": general_document,
            "passenger_general_document_list": passenger_general_document_list,
            "user": request.user,
        }
        data["passenger_general_document_list"] = render_to_string(
            "passenger_app_templates/passenger_details/passenger_general_document/create_document_list.html",
            context,
        )
        return JsonResponse(data)

    else:
        data["form_is_valid"] = False

    context = {
        "passenger_general_document_list": passenger_general_document_list,
        "general_document": general_document,
        "passenger": passenger,
    }

    if request.user.is_superuser:
        data["html_form"] = render_to_string(
            "passenger_app_templates/passenger_details/passenger_general_document/document_delete.html",
            context,
        )
        return JsonResponse(data)

    else:
        if user_groups is None:
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_delete":
                        data["html_form"] = render_to_string(
                            "passenger_app_templates/passenger_details/passenger_general_document/document_delete.html",
                            context,
                        )
                        return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)
