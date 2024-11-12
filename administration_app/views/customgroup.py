from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import JsonResponse
from administration_app.models import User, CustomGroup, Permissions
from administration_app.forms import CustomGroupCreationForm
from django.contrib.auth.decorators import login_required


@login_required
def customgroup(request):
    context = {}
    context["page_name"] = "Manage Groups"
    context["group_nav_link_status"] = "active"

    if request.user.is_superuser:
        group_list = CustomGroup.objects.all()
        context["group_list"] = group_list
        context["user"] = request.user

        return render(request, "CustomGroup/custom_group.html", context)
    else:
        return render(request, "errors/403.html", context)


# Create Custom Group
@login_required
def create_custom_group(request):
    data = dict()

    if request.method == "POST":
        form = CustomGroupCreationForm(request.POST)

        if form.is_valid():
            form.save()
            data["is_form_valid"] = True
            data["html_updated_permissions_list"] = render_to_string(
                "CustomGroup/custom_group_list.html",
                {
                    "group_list": CustomGroup.objects.all().order_by("-id"),
                    "user": request.user,
                },
            )
        else:
            data["is_form_valid"] = False
        return JsonResponse(data)
    else:
        context = {
            "form": CustomGroupCreationForm(),
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "CustomGroup/create_custom_group.html", context, request=request
        )
        return JsonResponse(data)


# Edit Custom Group
@login_required
def edit_custom_group(request, group_id):
    data = dict()
    role = CustomGroup.objects.get(id=group_id)
    if request.method == "POST":
        form = CustomGroupCreationForm(request.POST, instance=role)

        if form.is_valid():
            form.save()
            data["is_form_valid"] = True
            data["html_updated_permissions_list"] = render_to_string(
                "CustomGroup/custom_group_list.html",
                {
                    "group_list": CustomGroup.objects.all().order_by("-id"),
                    "user": request.user,
                },
            )
            return JsonResponse(data)
        else:
            data["is_form_valid"] = False
    else:
        context = {
            "form": CustomGroupCreationForm(instance=role),
            "role": role,
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "CustomGroup/edit_custom_group.html", context, request=request
        )
        return JsonResponse(data)


# Delete Custom Group
@login_required
def delete_custom_group(request, group_id):
    data = dict()
    if request.method == "POST":
        CustomGroup.objects.get(id=group_id).delete()
        data["is_form_valid"] = True
        data["html_updated_permissions_list"] = render_to_string(
            "CustomGroup/custom_group_list.html",
            {
                "group_list": CustomGroup.objects.all().order_by("-id"),
                "user": request.user,
            },
        )
        return JsonResponse(data)

    else:
        context = {
            "role": CustomGroup.objects.get(id=group_id),
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "CustomGroup/delete_custom_group.html", context, request=request
        )
        return JsonResponse(data)


# Custom Group Details Page
def customgroup_details(request, pk):
    customgroup = CustomGroup.objects.get(id=pk)
    context = {
        "page_name": "Manage Groups",
        "group_nav_link_status": "active",
        "group": customgroup,
        "user": request.user,
    }
    return render(request, "CustomGroup/customgroup_details.html", context)


# Add Users to the Custom Group.
@login_required
def add_group_members(request, pk):
    data = dict()
    group = CustomGroup.objects.get(id=pk)

    if request.method == "POST":
        group_members = request.POST.getlist("users")

        selected_users = User.objects.filter(id__in=group_members)
        group.group_users.add(*selected_users)

        data["form_is_valid"] = True
        data["html_updated_members_list"] = render_to_string(
            "CustomGroup/members_list.html",
            {
                "group": group,
                "user": request.user,
            },
        )
        return JsonResponse(data)
    else:
        alredy_exist_user = group.group_users.all()

        context = {
            "users": User.objects.exclude(id__in=alredy_exist_user),
            "group": CustomGroup.objects.get(id=pk),
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "CustomGroup/addMembers.html", context, request=request
        )
        return JsonResponse(data)


# Remove users from the custom group
@login_required
def remove_user_from_group(request, pk, member_id):
    data = dict()
    group = CustomGroup.objects.get(id=pk)

    selected_user = User.objects.get(id=member_id)

    if request.method == "POST":
        group.group_users.remove(member_id)

        data["form_is_valid"] = True
        data["html_updated_members_list"] = render_to_string(
            "CustomGroup/members_list.html",
            {
                "group": group,
                "user": request.user,
            },
        )
        return JsonResponse(data)

    else:
        context = {
            "user": User.objects.get(id=member_id),
            "group": CustomGroup.objects.get(id=pk),
            "selected_user": selected_user,
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "CustomGroup/remove_member.html", context, request=request
        )
        return JsonResponse(data)


# Add Permission To Custom Group
@login_required
def add_permissions(request, pk):
    data = dict()
    group = CustomGroup.objects.get(id=pk)

    existing_permissions = group.permissions.all()
    if request.method == "POST":
        group_permissions = request.POST.getlist("permissions")
        selected_permissions = Permissions.objects.filter(id__in=group_permissions)
        group.permissions.add(*selected_permissions)
        data["form_is_valid"] = True
        data["html_updated_permissions_list"] = render_to_string(
            "CustomGroup/permission_list.html",
            {
                "group": group,
                "user": request.user,
            },
        )
        return JsonResponse(data)
    else:
        context = {
            "permissions": Permissions.objects.exclude(id__in=existing_permissions),
            "group": CustomGroup.objects.get(id=pk),
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "CustomGroup/add_permission.html", context, request=request
        )
        return JsonResponse(data)


# Remove permission from the Custom Group
@login_required
def remove_permission_from_group(request, pk, permission_id):
    data = dict()
    group = CustomGroup.objects.get(id=pk)

    if request.method == "POST":
        group.permissions.remove(permission_id)
        data["form_is_valid"] = True
        data["html_updated_permissions_list"] = render_to_string(
            "CustomGroup/permission_list.html",
            {
                "group": group,
                "user": request.user,
            },
        )
        return JsonResponse(data)
    else:
        context = {
            "permission": Permissions.objects.get(id=permission_id),
            "group": CustomGroup.objects.get(id=pk),
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "CustomGroup/remove_permission.html", context, request=request
        )
        return JsonResponse(data)
