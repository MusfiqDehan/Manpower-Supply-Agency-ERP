from django.shortcuts import render
from passenger_app.forms import PassengerInfoSubmitForm
from passenger_app.models import Passenger, PassengerPassport
from django.contrib.auth.decorators import login_required

# agent_management_app
from agent_management_app.models import AgentInfo

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db import DatabaseError


# Passenger View
@login_required
def passenger_view(request):
    user_groups = request.user.Group_Users.all()
    if request.user.is_superuser:
        try:
            passenger_list = Passenger.objects.filter(
                fly_status=False,
                cancel_status=False,
                money_refund_status=False,
                status=True,
            ).order_by("-id")
        except DatabaseError as e:
            # Handle the database error here,
            pass

        context = {
            "page_name": "Ongoing Passengers",
            "ongoing_passenger_nav_link_status": "active",
            "passenger_list": passenger_list,
            "user": request.user,
        }

        return render(
            request,
            "passenger_app_templates/passenger_management/passenger_management.html",
            context,
        )
    else:
        if user_groups is None:
            return render(request, "errors/403.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "passenger_view":
                        try:
                            passenger_list = Passenger.objects.filter(
                                fly_status=False,
                                cancel_status=False,
                                money_refund_status=False,
                                status=True,
                            ).order_by("-id")
                        except DatabaseError as e:
                            # Handle the database error here,
                            pass

                        context = {
                            "page_name": "Ongoing Passengers",
                            "ongoing_passenger_nav_link_status": "active",
                            "passenger_list": passenger_list,
                            "user": request.user,
                        }

                        return render(
                            request,
                            "passenger_app_templates/passenger_management/passenger_management.html",
                            context,
                        )
            return render(request, "errors/403.html")


# Passenger create
@login_required
def passenger_create(request):
    data = {}
    agent_list = AgentInfo.objects.all()
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            form = PassengerInfoSubmitForm(request.POST, request.FILES)

            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()

                # Create and save the passport model
                passport = PassengerPassport(
                    passenger_passport=instance,
                    passport_number=instance.passport,
                    date_of_expairy=instance.passport_date_of_expairy,
                )
                passport.save()

                data["form_is_valid"] = True
                passenger_list = Passenger.objects.all().order_by("-id")
                context = {
                    "passenger_list": passenger_list,
                    "user": request.user,
                }
                data["html_passenger_list"] = render_to_string(
                    "passenger_app_templates/passenger_management/passenger_list.html",
                    context,
                )
                return JsonResponse(data)

            else:
                data["form_is_valid"] = False
                return JsonResponse(data)
        else:
            agent_id = request.GET.get("selected_agent_middleman_value")
            if agent_id:
                agent = AgentInfo.objects.get(id=agent_id)
                middleman_list = agent.agent_middleman.all()

                context = {
                    "middleman_list": middleman_list,
                }
                data["selected_middleman_list"] = render_to_string(
                    "passenger_app_templates/passenger_management/agent_middleman_list.html",
                    context,
                )
                return JsonResponse(data)

            else:
                # Handle the GET request (initial form load)
                form = PassengerInfoSubmitForm()

            context = {
                "form": form,
                "agent_list": agent_list,
                "user": request.user,
            }

            data["html_form"] = render_to_string(
                "passenger_app_templates/passenger_management/create_passenger.html",
                context,
                request=request,
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
                    if perm.codename == "passenger_create":
                        if request.method == "POST":
                            form = PassengerInfoSubmitForm(request.POST, request.FILES)

                            if form.is_valid():
                                instance = form.save(commit=False)
                                instance.save()

                                # Create and save the passport model
                                passport = PassengerPassport(
                                    passenger_passport=instance,
                                    passport_number=instance.passport,
                                    date_of_expairy=instance.passport_date_of_expairy,
                                )
                                passport.save()

                                data["form_is_valid"] = True
                                passenger_list = Passenger.objects.all().order_by("-id")
                                context = {
                                    "passenger_list": passenger_list,
                                    "user": request.user,
                                }
                                data["html_passenger_list"] = render_to_string(
                                    "passenger_app_templates/passenger_management/passenger_list.html",
                                    context,
                                )
                                return JsonResponse(data)

                            else:
                                data["form_is_valid"] = False
                                return JsonResponse(data)
                        else:
                            agent_id = request.GET.get("selected_agent_middleman_value")
                            if agent_id:
                                agent = AgentInfo.objects.get(id=agent_id)
                                middleman_list = agent.agent_middleman.all()

                                context = {
                                    "middleman_list": middleman_list,
                                }
                                data["selected_middleman_list"] = render_to_string(
                                    "passenger_app_templates/passenger_management/agent_middleman_list.html",
                                    context,
                                )
                                return JsonResponse(data)

                            else:
                                # Handle the GET request (initial form load)
                                form = PassengerInfoSubmitForm()

                                context = {
                                    "form": form,
                                    "agent_list": agent_list,
                                    "user": request.user,
                                }

                                data["html_form"] = render_to_string(
                                    "passenger_app_templates/passenger_management/create_passenger.html",
                                    context,
                                    request=request,
                                )
                                return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


# Passenger Edit
@login_required
def passenger_edit(request, pk):
    data = {}
    agent_lists = AgentInfo.objects.all()
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if pk:
            passenger = Passenger.objects.get(id=pk)
        else:
            passenger = None

        if request.method == "POST":
            form = PassengerInfoSubmitForm(
                request.POST, request.FILES, instance=passenger
            )
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                data["form_is_valid"] = True
                passenger_list = Passenger.objects.all().order_by("-id")
                data["html_passenger_list"] = render_to_string(
                    "passenger_app_templates/passenger_management/passenger_list.html",
                    {
                        "passenger_list": passenger_list,
                        "user": request.user,
                    },
                )
                return JsonResponse(data)
            else:
                data["form_is_valid"] = False
                return JsonResponse(data)
        else:
            agent_id = request.GET.get("selected_agent_middleman_value")
            if agent_id:
                agent = AgentInfo.objects.get(id=agent_id)
                middleman_list = agent.agent_middleman.all()
                context = {
                    "middleman_list": middleman_list,
                }
                data["selected_middleman_list"] = render_to_string(
                    "passenger_app_templates/passenger_management/agent_middleman_list.html",
                    context,
                )
                return JsonResponse(data)
            else:
                form = PassengerInfoSubmitForm(instance=passenger)

            context = {
                "form": form,
                "passenger": passenger,
                "agent_list": agent_lists,
                "user": request.user,
            }
            data["html_form"] = render_to_string(
                "passenger_app_templates/passenger_management/edit_passenger.html",
                context,
                request=request,
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
                    if perm.codename == "passenger_update":
                        if pk:
                            passenger = Passenger.objects.get(id=pk)
                        else:
                            passenger = None

                        if request.method == "POST":
                            form = PassengerInfoSubmitForm(
                                request.POST, request.FILES, instance=passenger
                            )
                            if form.is_valid():
                                instance = form.save(commit=False)
                                instance.save()
                                data["form_is_valid"] = True
                                passenger_list = Passenger.objects.all().order_by("-id")
                                data["html_passenger_list"] = render_to_string(
                                    "passenger_app_templates/passenger_management/passenger_list.html",
                                    {
                                        "passenger_list": passenger_list,
                                        "user": request.user,
                                    },
                                )
                                return JsonResponse(data)
                            else:
                                data["form_is_valid"] = False
                                return JsonResponse(data)
                        else:
                            agent_id = request.GET.get("selected_agent_middleman_value")
                            if agent_id:
                                agent = AgentInfo.objects.get(id=agent_id)
                                middleman_list = agent.agent_middleman.all()
                                context = {
                                    "middleman_list": middleman_list,
                                }
                                data["selected_middleman_list"] = render_to_string(
                                    "passenger_app_templates/passenger_management/agent_middleman_list.html",
                                    context,
                                )
                                return JsonResponse(data)
                            else:
                                form = PassengerInfoSubmitForm(instance=passenger)

                            context = {
                                "form": form,
                                "passenger": passenger,
                                "agent_list": agent_lists,
                                "user": request.user,
                            }
                            data["html_form"] = render_to_string(
                                "passenger_app_templates/passenger_management/edit_passenger.html",
                                context,
                                request=request,
                            )
                            return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


# Passenger Delete
@login_required
def passenger_delete(request, pk):
    data = {}
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        try:
            passenger = Passenger.objects.get(id=pk)
        except Passenger.DoesNotExist:
            data["form_is_valid"] = False
            return JsonResponse(data)

        if request.method == "POST":
            passenger.delete()
            data["form_is_valid"] = True
            passenger_list = Passenger.objects.all().order_by("-id")
            data["html_passenger_list"] = render_to_string(
                "passenger_app_templates/passenger_management/passenger_list.html",
                {
                    "passenger_list": passenger_list,
                    "user": request.user,
                },
            )
        else:
            data["form_is_valid"] = False

        context = {"passenger": passenger}
        data["html_form"] = render_to_string(
            "passenger_app_templates/passenger_management/delete_passenger.html",
            context,
            request=request,
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
                    if perm.codename == "passenger_delete":
                        try:
                            passenger = Passenger.objects.get(id=pk)
                        except Passenger.DoesNotExist:
                            data["form_is_valid"] = False
                            return JsonResponse(data)

                        if request.method == "POST":
                            passenger.delete()
                            data["form_is_valid"] = True
                            passenger_list = Passenger.objects.all().order_by("-id")
                            data["html_passenger_list"] = render_to_string(
                                "passenger_app_templates/passenger_management/passenger_list.html",
                                {
                                    "passenger_list": passenger_list,
                                    "user": request.user,
                                },
                            )
                        else:
                            data["form_is_valid"] = False

                        context = {"passenger": passenger}
                        data["html_form"] = render_to_string(
                            "passenger_app_templates/passenger_management/delete_passenger.html",
                            context,
                            request=request,
                        )
                        return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)
