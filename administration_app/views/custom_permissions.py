from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import PermissionApp, CustomGroup


@login_required
def add_group_permissions(request, group_id):
    context = {}
    data = {}

    permissions = PermissionApp.objects.all()
    user = request.user
    user_group = get_object_or_404(CustomGroup, id=group_id)
    selected_permissions = user_group.permissions.all()

    context["permissions"] = permissions
    context["selected_permissions"] = selected_permissions
    context["group"] = user_group  # Ensure group is passed to the context

    data["valid"] = False
    data["add_permissions_form"] = render_to_string(
        "CustomGroup/permissions_form.html", context, request=request
    )
    data["permission_list"] = render_to_string(
        "CustomGroup/permission_list.html", context, request=request
    )
    data["spinner"] = render_to_string("spinner.html", context, request=request)

    if request.method == "POST":
        data["valid"] = True
        permissions_list = request.POST.getlist("permission_id")

        # Convert permissions_list to a set of integers
        permissions_set = set(map(int, permissions_list))

        # Add new permissions
        for perm_id in permissions_set:
            if not selected_permissions.filter(id=perm_id).exists():
                user_group.permissions.add(perm_id)

        # Remove unchecked permissions
        for perm in selected_permissions:
            if perm.id not in permissions_set:
                user_group.permissions.remove(perm.id)

        # Update the context with the new selected permissions
        context["selected_permissions"] = user_group.permissions.all()
        data["permission_list"] = render_to_string(
            "CustomGroup/permission_list.html", context, request=request
        )

        return JsonResponse(data)

    return JsonResponse(data)
