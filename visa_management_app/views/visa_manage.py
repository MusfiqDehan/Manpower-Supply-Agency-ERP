from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from agent_management_app.models import AgentInfo
from django.contrib.auth.decorators import login_required


from visa_management_app.models import Visa
from visa_management_app.forms import VisaCreateForm


# Visa Management
@login_required
def VisaManage(request):
    user_groups = request.user.Group_Users.all()
    if request.user.is_superuser:
        visa_list = Visa.objects.all().order_by("-id")
        context = {
            "page_name": "Visa",
            "visa_nav_link_status": "active",
            "visa_list": visa_list,
        }
        return render(request, "visa/visa_manage.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html")

        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                print(group_permissions)

                for perm in group_permissions:
                    print("print3")
                    if perm.codename == "visa_view":
                        visa_list = Visa.objects.all().order_by("-id")
                        context = {
                            "page_name": "Visa",
                            "visa_nav_link_status": "active",
                            "visa_list": visa_list,
                        }
                        return render(request, "visa/visa_manage.html", context)

            return render(request, "errors/403.html")


# Create
def Visa_create(request):
    data = {}
    visa_list = Visa.objects.all()

    if request.method == "POST":
        print("post the form...")
        form = VisaCreateForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            data["form_is_valid"] = True

            visa_list = Visa.objects.all().order_by("-id")
            context = {
                "visa_list": visa_list,
            }

            data["html_visa_list"] = render_to_string(
                "visa/visa_list.html", context, request=request
            )
            return JsonResponse(data)

        else:
            print(form.errors)
            data["form_is_valid"] = False
            return JsonResponse(data)

    else:
        form = VisaCreateForm()

        context = {
            "form": form,
            "visa_list": visa_list,
            "user": request.user,
        }

        data["html_form"] = render_to_string(
            "visa/visa_create.html", context, request=request
        )

        user_groups = request.user.Group_Users.all()

        if request.user.is_superuser:
            data["html_form"] = render_to_string(
                "visa/visa_create.html", context, request=request
            )

            return JsonResponse(data)
        else:
            if user_groups is None:
                data["html_form"] = render_to_string(
                    "errors/403-contents.html", context, request=request
                )

                return JsonResponse(data)

            else:
                for user_group in user_groups:
                    group_permissions = user_group.permissions.all()

                    for perm in group_permissions:
                        if perm.codename == "visa_create":
                            data["html_form"] = render_to_string(
                                "visa/visa_create.html", context, request=request
                            )

                            return JsonResponse(data)

                data["html_form"] = render_to_string(
                    "errors/403-contents.html", context, request=request
                )

                return JsonResponse(data)


# Visa Edit.
@login_required
def visa_edit(request, pk):
    data = dict()
    visa = Visa.objects.get(pk=pk)

    if request.method == "POST":
        form = VisaCreateForm(request.POST, request.FILES, instance=visa)
        if form.is_valid():
            form.save()
            data["form_is_valid"] = True
            visa_list = Visa.objects.all().order_by("-id")
            context = {
                "visa_list": visa_list,
            }
            data["html_visa_list"] = render_to_string(
                "visa/visa_list.html", context, request=request
            )
            return JsonResponse(data)
        else:
            data["form_is_valid"] = False
            return JsonResponse(data)
    else:
        form = VisaCreateForm(instance=visa)
        context = {
            "form": form,
            "visa": visa,
            "user": request.user,
        }

    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        data["html_form"] = render_to_string(
            "visa/visa_edit.html", context, request=request
        )
        return JsonResponse(data)
    else:
        if user_groups is None:
            data["html_form"] = render_to_string(
                "errors/403-contents.html", context, request=request
            )
            return JsonResponse(data)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "visa_update":
                        data["html_form"] = render_to_string(
                            "visa/visa_edit.html", context, request=request
                        )
                        return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", context, request=request
            )
            return JsonResponse(data)


# Delete
@login_required
def visa_delete(request, pk):
    data = {}
    try:
        visa = Visa.objects.get(pk=pk)
    except Visa.DoesNotExist:
        data["form_is_valid"] = False
        return JsonResponse(data)

    if request.method == "POST":
        visa.delete()
        data["form_is_valid"] = True
        visa_list = Visa.objects.all().order_by("-id")
        context = {
            "visa_list": visa_list,
        }
        data["html_visa_list"] = render_to_string(
            "visa/visa_list.html", context, request=request
        )
        return JsonResponse(data)
    else:
        data["form_is_valid"] = False

    context = {
        "visa": visa,
    }

    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        data["html_form"] = render_to_string(
            "visa/visa_delete.html", context, request=request
        )
        return JsonResponse(data)
    else:
        if user_groups is None:
            data["html_form"] = render_to_string(
                "errors/403-contents.html", context, request=request
            )
            return JsonResponse(data)
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "visa_delete":
                        data["html_form"] = render_to_string(
                            "visa/visa_delete.html", context, request=request
                        )
                        return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", context, request=request
            )
            return JsonResponse(data)
