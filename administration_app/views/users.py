from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from administration_app.models import User
from administration_app.forms import SuperuserChangePasswordForm, RegistrationForm


# ------------------------------ All Users ----------------------------------


# User Default page.
@login_required
def all_users(request):
    context = {}
    context["page_name"] = "Manage Users"
    context["user_nav_link_status"] = "active"

    if request.user.is_superuser:
        all_users_list = User.objects.filter(is_superuser=False).order_by("-id")

        context["all_users_list"] = all_users_list
        context["user"] = request.user

        return render(request, "users/users.html", context)
    else:
        return render(request, "errors/403.html", context)


@login_required
def user_registration(request):
    data = dict()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                data["is_form_valid"] = True
                users = User.objects.filter(is_superuser=False).order_by("-date_joined")
                context = {
                    "all_users_list": users,
                    "user": request.user,
                }
                data["html_updated_user_list"] = render_to_string(
                    "users/user_list.html", context, request=request
                )
                return JsonResponse(data)
            except IntegrityError as e:
                if "unique constraint" in str(e):
                    form.add_error("email", "A user with this email already exists.")
                data["is_form_valid"] = False
                data["form_errors"] = form.errors.as_json()
                return JsonResponse(data)
        else:
            data["is_form_valid"] = False
            data["form_errors"] = form.errors.as_json()
            return JsonResponse(data)

    else:
        form = RegistrationForm()
        data["html_form"] = render_to_string(
            "users/user_registration.html", {"form": form}, request=request
        )
    return JsonResponse(data)


# --------------------- User Password Change (All User Can Change the password) -------------
@login_required
# @user_passes_test(lambda u: u.is_superuser) # Only Super Admin Can Change Password.
def user_change_password(request, user_id):
    data = dict()
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = SuperuserChangePasswordForm(request.POST)

        if form.is_valid():
            form.save(user=user)

            data["is_form_valid"] = True
            data["html_updated_user_list"] = render_to_string(
                "users/user_list.html",
                {
                    "all_users_list": User.objects.filter(is_superuser=False).order_by(
                        "-date_joined"
                    ),
                    "user": request.user,
                },
            )
            return JsonResponse(data)
        else:
            data["is_form_valid"] = False
            return JsonResponse(data)
    else:
        context = {
            "form": SuperuserChangePasswordForm(),
            "user_id": user,
            "user": request.user,
        }
        data["html_form"] = render_to_string(
            "users/user_change_password.html", context, request=request
        )
        return JsonResponse(data)


# ------------------------------ User Deleted  ----------------------------------
@login_required
def delete_user(request, user_id):
    data = dict()
    selected_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        selected_user.delete()
        data["is_form_valid"] = True

        users = User.objects.filter(is_superuser=False).order_by("-date_joined")

        context = {
            "all_users_list": users,
            "user": request.user,
        }
        data["html_updated_user_list"] = render_to_string(
            "users/user_list.html", context
        )
        return JsonResponse(data)
    else:
        data["html_form"] = render_to_string(
            "users/user_delete.html",
            {
                "selected_user": selected_user,
                "user": request.user,
            },
            request=request,
        )
        return JsonResponse(data)


@login_required
@require_POST
def change_user_status(request):
    user_id = request.POST.get("user_id")
    action_type = request.POST.get("action_type")
    action_value = request.POST.get("action_value")

    user = get_object_or_404(User, id=user_id)

    if action_type == "status":
        user.is_active = action_value == "activate"
    elif action_type == "role":
        user.is_staff = action_value == "super"

    user.save()

    return JsonResponse({"success": True})
