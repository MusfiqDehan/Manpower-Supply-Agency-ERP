from django.shortcuts import render, get_object_or_404

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from company_documentation_app.forms import CompanyDocumentCategoryForm
from company_documentation_app.models import CompanyDocumentCategory


@login_required
def company_document_category(request):
    context = {}
    context["page_name"] = "Company Document Category"
    context["company_document_category_nav_link_status"] = "active"

    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        company_document_category_list = CompanyDocumentCategory.objects.all().order_by(
            "-id"
        )

        context["company_document_category_list"] = company_document_category_list

        return render(
            request, "company_document_category/company_document_category.html", context
        )
    else:
        if user_groups is None:
            return render(request, "errors/403.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_category_view":
                        company_document_category_list = (
                            CompanyDocumentCategory.objects.all().order_by("-id")
                        )
                        context["company_document_category_list"] = (
                            company_document_category_list
                        )
                        return render(
                            request,
                            "company_document_category/company_document_category.html",
                            context,
                        )
            return render(request, "errors/403.html")


@login_required
def company_document_category_create(request):
    data = {}
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            form = CompanyDocumentCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data["form_is_valid"] = True
                company_document_category_list = (
                    CompanyDocumentCategory.objects.all().order_by("-id")
                )
                context = dict(
                    company_document_category_list=company_document_category_list
                )
                data["company_document_category"] = render_to_string(
                    "company_document_category/company_document_category_list.html",
                    context,
                    request=request,
                )
                return JsonResponse(data)
            else:
                data["form_is_valid"] = False
                data["html_form"] = render_to_string(
                    "company_document_category/company_document_category_create.html",
                    request=request,
                )
                return JsonResponse(data)
        else:
            data["html_form"] = render_to_string(
                "company_document_category/company_document_category_create.html",
                request=request,
            )
            return JsonResponse(data)
    else:
        if user_groups is None:
            return render(request, "errors/403-contents.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_category_create":
                        if request.method == "POST":
                            form = CompanyDocumentCategoryForm(
                                request.POST, request.FILES
                            )
                            if form.is_valid():
                                form.save()
                                data["form_is_valid"] = True
                                company_document_category_list = (
                                    CompanyDocumentCategory.objects.all().order_by(
                                        "-id"
                                    )
                                )
                                context = dict(
                                    company_document_category_list=company_document_category_list
                                )
                                data["company_document_category"] = render_to_string(
                                    "company_document_category/company_document_category_list.html",
                                    context,
                                    request=request,
                                )
                                return JsonResponse(data)
                            else:
                                data["form_is_valid"] = False
                                data["html_form"] = render_to_string(
                                    "company_document_category/company_document_category_create.html",
                                    request=request,
                                )
                                return JsonResponse(data)
                        else:
                            data["html_form"] = render_to_string(
                                "company_document_category/company_document_category_create.html",
                                request=request,
                            )
                            return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


@login_required
def company_document_category_edit(request, pk):
    data = dict()
    document_category = CompanyDocumentCategory.objects.get(pk=pk)
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            form = CompanyDocumentCategoryForm(
                request.POST, request.FILES, instance=document_category
            )
            if form.is_valid():
                form.save()
                data["form_is_valid"] = True
                company_document_category_list = (
                    CompanyDocumentCategory.objects.all().order_by("-id")
                )
                context = dict(
                    company_document_category_list=company_document_category_list
                )
                data["company_document_category"] = render_to_string(
                    "company_document_category/company_document_category_list.html",
                    context,
                    request=request,
                )
                return JsonResponse(data)
            else:
                data["form_is_valid"] = False
                return JsonResponse(data)
        else:
            context = dict(company_document_category=document_category)
            data["html_form"] = render_to_string(
                "company_document_category/company_document_category_edit.html",
                context,
                request=request,
            )
            return JsonResponse(data)
    else:
        if user_groups is None:
            return render(request, "errors/403-contents.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_category_update":
                        if request.method == "POST":
                            form = CompanyDocumentCategoryForm(
                                request.POST, request.FILES, instance=document_category
                            )
                            if form.is_valid():
                                form.save()
                                data["form_is_valid"] = True
                                company_document_category_list = (
                                    CompanyDocumentCategory.objects.all().order_by(
                                        "-id"
                                    )
                                )
                                context = dict(
                                    company_document_category_list=company_document_category_list
                                )
                                data["company_document_category"] = render_to_string(
                                    "company_document_category/company_document_category_list.html",
                                    context,
                                    request=request,
                                )
                                return JsonResponse(data)
                            else:
                                data["form_is_valid"] = False
                                return JsonResponse(data)
                        else:
                            context = dict(company_document_category=document_category)
                            data["html_form"] = render_to_string(
                                "company_document_category/company_document_category_edit.html",
                                context,
                                request=request,
                            )
                            return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


@login_required
def company_document_category_delete(request, pk):
    data = dict()
    document_category = get_object_or_404(CompanyDocumentCategory, pk=pk)
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            document_category.delete()
            data["form_is_valid"] = True
            company_document_category_list = (
                CompanyDocumentCategory.objects.all().order_by("-id")
            )
            context = dict(
                company_document_category_list=company_document_category_list
            )
            data["company_document_category"] = render_to_string(
                "company_document_category/company_document_category_list.html",
                context,
                request=request,
            )
            return JsonResponse(data)
        else:
            context = dict(company_document_category=document_category)
            data["html_form"] = render_to_string(
                "company_document_category/company_document_category_delete.html",
                context,
                request=request,
            )
            return JsonResponse(data)
    else:
        if user_groups is None:
            return render(request, "errors/403-contents.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "document_category_delete":
                        if request.method == "POST":
                            document_category.delete()
                            data["form_is_valid"] = True
                            company_document_category_list = (
                                CompanyDocumentCategory.objects.all().order_by("-id")
                            )
                            context = dict(
                                company_document_category_list=company_document_category_list
                            )
                            data["company_document_category"] = render_to_string(
                                "company_document_category/company_document_category_list.html",
                                context,
                                request=request,
                            )
                            return JsonResponse(data)
                        else:
                            context = dict(company_document_category=document_category)
                            data["html_form"] = render_to_string(
                                "company_document_category/company_document_category_delete.html",
                                context,
                                request=request,
                            )
                            return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)
