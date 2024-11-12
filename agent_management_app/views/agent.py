import re
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from agent_management_app.forms import AgentInfoSubmitForm
from agent_management_app.models import AgentInfo, AgentAccount
from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse


# Agent View
@login_required
def agent_view(request):
    context = {}

    context["page_name"] = "Agent"
    context["agent_nav_link_status"] = "active"
    context["agent_list"] = AgentInfo.objects.filter(status=True).order_by("id")

    user_groups = request.user.Group_Users.all()
    if request.user.is_superuser:
        context["user"] = request.user
        context["agent_list"] = AgentInfo.objects.filter(status=True).order_by("id")

        return render(request, "agent_management/agent/agent.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html", context)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "agent_view":
                        agent_list = AgentInfo.objects.filter(status=True).order_by(
                            "id"
                        )

                        context["agent_list"] = agent_list
                        context["user"] = request.user
                        return render(
                            request, "agent_management/agent/agent.html", context
                        )
            return render(request, "errors/403.html", context)


# Reusable function for saving the form
def save_agent_form(request, form, template_name):
    data = dict()
    user_groups = request.user.Group_Users.all()
    if request.method == "POST":
        if form.is_valid():
            form.save()

            data["form_is_valid"] = True

            agent_list = AgentInfo.objects.filter(status=True).order_by("id")

            data["html_agent_list"] = render_to_string(
                "agent_management/agent/agent_list.html",
                {
                    "agent_list": agent_list,
                    "user": request.user,
                },
            )

        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
        "user": request.user,
    }
    if request.user.is_superuser:
        data["html_form"] = render_to_string(template_name, context, request=request)
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
                    if perm.codename == "agent_create":
                        data["html_form"] = render_to_string(
                            template_name, context, request=request
                        )
                        return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


# Agent Create/Add
@login_required
def agent_add(request):
    if request.method == "POST":
        form = AgentInfoSubmitForm(request.POST, request.FILES)
    else:
        form = AgentInfoSubmitForm()
    return save_agent_form(request, form, "agent_management/agent/create_agent.html")


# Edit part ( have to make a separate save view for edit bcoz of the details page-edit btn)
# Agent Profile Edit
def save_agent_edit_form(request, form, agent, template_name):
    data = dict()
    user_groups = request.user.Group_Users.all()
    if request.method == "POST":
        if form.is_valid():
            form.save()

            data["form_is_valid"] = True

            agent_list = AgentInfo.objects.filter(status=True).order_by("id")

            data["html_agent_list"] = render_to_string(
                "agent_management/agent/agent_list.html",
                {
                    "agent_list": agent_list,
                    "user": request.user,
                },
            )
            data["html_agent_card_1"] = render_to_string(
                "agent_management/agent_details/agent_card_1.html",
                {
                    "agent": agent,
                    "user": request.user,
                },
            )
            data["html_agent_card_2"] = render_to_string(
                "agent_management/agent_details/agent_card_2.html",
                {
                    "agent": agent,
                    "user": request.user,
                },
            )

        else:
            data["form_is_valid"] = False

    context = {
        "form": form,
        "agent": agent,
        "user": request.user,
    }

    if request.user.is_superuser:
        data["html_form"] = render_to_string(template_name, context, request=request)
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
                    if perm.codename == "agent_update":
                        data["html_form"] = render_to_string(
                            template_name, context, request=request
                        )
                        return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


@login_required
def agent_edit(request, pk):
    agent = AgentInfo.objects.get(id=pk)

    if request.method == "POST":
        form = AgentInfoSubmitForm(request.POST, request.FILES, instance=agent)
    else:
        form = AgentInfoSubmitForm(instance=agent)
    return save_agent_edit_form(
        request, form, agent, "agent_management/agent/edit_agent.html"
    )


# Ajax passenger information delete form
def save_agent_delete_form(request, agent, template_name):
    data = dict()
    user_groups = request.user.Group_Users.all()

    object = agent

    if request.method == "POST":
        object.delete()

        data["form_is_valid"] = True

        agent_list = AgentInfo.objects.filter(status=True).order_by("id")

        data["html_agent_list"] = render_to_string(
            "agent_management/agent/agent_list.html",
            {
                "agent_list": agent_list,
                "user": request.user,
            },
        )

    else:
        data["form_is_valid"] = False

    context = {
        "agent": agent,
        "user": request.user,
    }

    if request.user.is_superuser:
        data["html_form"] = render_to_string(template_name, context, request=request)
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
                    if perm.codename == "agent_delete":
                        data["html_form"] = render_to_string(
                            template_name, context, request=request
                        )
                        return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


@login_required
def agent_delete(request, pk):
    agent = AgentInfo.objects.get(id=pk)
    return save_agent_delete_form(
        request, agent, "agent_management/agent/delete_agent.html"
    )
