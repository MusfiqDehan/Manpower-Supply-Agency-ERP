from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

from company_documentation_app.models import CompanyDocument, CompanyDocumentCategory
from company_documentation_app.forms import CompanyDocumentForm


@login_required
def document_list_view(request):
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        company_document_list = CompanyDocument.objects.all().order_by("-id")
        context = {
            "page_name": "Company Document",
            "company_document_nav_link_status": "active",
            "company_document_list": company_document_list,
            "user": request.user,
        }
        return render(request, "company_document/company_document.html", context)
    else:
        if user_groups is None:
            return render(request, "errors/403.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_view":
                        company_document_list = CompanyDocument.objects.all().order_by(
                            "-id"
                        )
                        context = {
                            "page_name": "Company Document",
                            "company_document_nav_link_status": "active",
                            "company_document_list": company_document_list,
                            "user": request.user,
                        }
                        return render(
                            request, "company_document/company_document.html", context
                        )

            return render(request, "errors/403.html")


@login_required
def document_create(request):
    data = {}
    user_groups = request.user.Group_Users.all()
    company_document_category_list = CompanyDocumentCategory.objects.all()

    if request.user.is_superuser:
        if request.method == "POST":
            form = CompanyDocumentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data["form_is_valid"] = True
                company_document_list = CompanyDocument.objects.all().order_by("-id")
                context = {
                    "company_document_list": company_document_list,
                    "user": request.user,
                    "company_document_category_list": company_document_category_list,
                }
                data["company_document_data"] = render_to_string(
                    "company_document/create_document_list.html", context
                )
                return JsonResponse(data)
            else:
                data["form_is_valid"] = False
                return JsonResponse(data)
        else:
            form = CompanyDocumentForm()
            context = {
                "form": form,
                "user": request.user,
                "company_document_category_list": company_document_category_list,
            }
            data["html_form"] = render_to_string(
                "company_document/create_document.html", context
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
                            form = CompanyDocumentForm(request.POST, request.FILES)
                            if form.is_valid():
                                form.save()
                                data["form_is_valid"] = True
                                company_document_list = (
                                    CompanyDocument.objects.all().order_by("-id")
                                )
                                context = {
                                    "company_document_list": company_document_list,
                                    "user": request.user,
                                    "company_document_category_list": company_document_category_list,
                                }
                                data["company_document_data"] = render_to_string(
                                    "company_document/create_document_list.html",
                                    context,
                                )
                                return JsonResponse(data)
                            else:
                                data["form_is_valid"] = False
                                return JsonResponse(data)
                        else:
                            form = CompanyDocumentForm()
                            context = {
                                "form": form,
                                "user": request.user,
                                "company_document_category_list": company_document_category_list,
                            }
                            data["html_form"] = render_to_string(
                                "company_document/create_document.html", context
                            )
                            return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


def document_edit(request, pk):
    data = dict()

    user_groups = request.user.Group_Users.all()
    company_document_category_list = CompanyDocumentCategory.objects.all()
    selected_obj = CompanyDocument.objects.get(pk=pk)

    if request.method == "POST":
        form = CompanyDocumentForm(request.POST, request.FILES, instance=selected_obj)
        if form.is_valid():
            form.save()

            data["form_is_valid"] = True
            company_document_list = CompanyDocument.objects.all().order_by("-id")
            context = {
                "company_document_list": company_document_list,
                "company_document_category_list": company_document_category_list,
                "user": request.user,
                "selected_obj": selected_obj,
            }
            data["company_document_data"] = render_to_string(
                "company_document/create_document_list.html", context
            )
            return JsonResponse(data)

        else:
            data["form_is_valid"] = False
            return JsonResponse(data)

    else:
        form = CompanyDocumentForm(instance=selected_obj)

        context = {
            "form": form,
            "selected_obj": selected_obj,
            "user": request.user,
            "company_document_category_list": company_document_category_list,
        }

    if request.user.is_superuser:
        data["html_form"] = render_to_string(
            "company_document/document_edit.html", context
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
                            "company_document/document_edit.html", context
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
    try:
        selected_obj = CompanyDocument.objects.get(pk=pk)

    except selected_obj.DoesNotExist:
        data["form_is_valid"] = False
        return JsonResponse(data)

    if request.method == "POST":
        selected_obj.delete()

        data["form_is_valid"] = True
        company_document_list = CompanyDocument.objects.all().order_by("-id")
        context = {
            "company_document_list": company_document_list,
            "user": request.user,
        }
        data["company_document_data"] = render_to_string(
            "company_document/create_document_list.html", context
        )
        return JsonResponse(data)

    else:
        data["form_is_valid"] = False

    context = {
        "selected_obj": selected_obj,
    }

    if request.user.is_superuser:
        data["html_form"] = render_to_string(
            "company_document/document_delete.html", context
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
                            "company_document/document_delete.html", context
                        )
                        return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)
