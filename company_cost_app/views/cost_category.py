from django.shortcuts import render

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from company_cost_app.forms import CostCategoryForm
from company_cost_app.models import CostCategory


@login_required
def company_cost_category(request):
    context = {}
    context["page_name"] = "Cost Category"
    context["company_cost_category_nav_link_status"] = "active"

    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        company_cost_category_list = CostCategory.objects.all().order_by("-id")

        context["company_cost_category_list"] = company_cost_category_list

        return render(
            request, "company_cost_category/company_cost_category.html", context
        )
    else:
        if user_groups is None:
            return render(request, "errors/403.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "cost_category_view":
                        company_cost_category_list = (
                            CostCategory.objects.all().order_by("-id")
                        )
                        context["company_cost_category_list"] = (
                            company_cost_category_list
                        )
                        return render(
                            request,
                            "company_cost_category/company_cost_category.html",
                            context,
                        )
            return render(request, "errors/403.html")


@login_required
def company_cost_category_create(request):
    data = {}
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            form = CostCategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                data["form_is_valid"] = True
                company_cost_category_list = CostCategory.objects.all().order_by("-id")
                context = dict(company_cost_category_list=company_cost_category_list)
                data["company_cost_category"] = render_to_string(
                    "company_cost_category/company_cost_category_list.html",
                    context,
                    request=request,
                )
                return JsonResponse(data)
            else:
                data["form_is_valid"] = False
                data["html_form"] = render_to_string(
                    "company_cost_category/company_cost_category_create.html",
                    request=request,
                )
                return JsonResponse(data)
        else:
            data["html_form"] = render_to_string(
                "company_cost_category/company_cost_category_create.html",
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
                    if perm.codename == "cost_category_create":
                        if request.method == "POST":
                            form = CostCategoryForm(request.POST, request.FILES)
                            if form.is_valid():
                                form.save()
                                data["form_is_valid"] = True
                                company_cost_category_list = (
                                    CostCategory.objects.all().order_by("-id")
                                )
                                context = dict(
                                    company_cost_category_list=company_cost_category_list
                                )
                                data["company_cost_category"] = render_to_string(
                                    "company_cost_category/company_cost_category_list.html",
                                    context,
                                    request=request,
                                )
                                return JsonResponse(data)
                            else:
                                data["form_is_valid"] = False
                                data["html_form"] = render_to_string(
                                    "company_cost_category/company_cost_category_create.html",
                                    request=request,
                                )
                                return JsonResponse(data)
                        else:
                            data["html_form"] = render_to_string(
                                "company_cost_category/company_cost_category_create.html",
                                request=request,
                            )
                            return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


@login_required
def company_cost_category_edit(request, pk):
    data = dict()
    cost_category = CostCategory.objects.get(pk=pk)
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            form = CostCategoryForm(request.POST, request.FILES, instance=cost_category)
            if form.is_valid():
                form.save()
                data["form_is_valid"] = True
                company_cost_category_list = CostCategory.objects.all().order_by("-id")
                context = dict(company_cost_category_list=company_cost_category_list)
                data["company_cost_category"] = render_to_string(
                    "company_cost_category/company_cost_category_list.html",
                    context,
                    request=request,
                )
                return JsonResponse(data)
            else:
                data["form_is_valid"] = False
                return JsonResponse(data)
        else:
            context = dict(company_cost_category=cost_category)
            data["html_form"] = render_to_string(
                "company_cost_category/company_cost_category_edit.html",
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
                    if perm.codename == "cost_category_update":
                        if request.method == "POST":
                            form = CostCategoryForm(
                                request.POST, request.FILES, instance=cost_category
                            )
                            if form.is_valid():
                                form.save()
                                data["form_is_valid"] = True
                                company_cost_category_list = (
                                    CostCategory.objects.all().order_by("-id")
                                )
                                context = dict(
                                    company_cost_category_list=company_cost_category_list
                                )
                                data["company_cost_category"] = render_to_string(
                                    "company_cost_category/company_cost_category_list.html",
                                    context,
                                    request=request,
                                )
                                return JsonResponse(data)
                            else:
                                data["form_is_valid"] = False
                                return JsonResponse(data)
                        else:
                            context = dict(company_cost_category=cost_category)
                            data["html_form"] = render_to_string(
                                "company_cost_category/company_cost_category_edit.html",
                                context,
                                request=request,
                            )
                            return JsonResponse(data)
            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)


@login_required
def company_cost_category_delete(request, pk):
    data = dict()
    cost_category = CostCategory.objects.get(pk=pk)
    user_groups = request.user.Group_Users.all()

    if request.user.is_superuser:
        if request.method == "POST":
            cost_category.delete()
            data["form_is_valid"] = True
            company_cost_category_list = CostCategory.objects.all().order_by("-id")
            context = dict(company_cost_category_list=company_cost_category_list)
            data["company_cost_category"] = render_to_string(
                "company_cost_category/company_cost_category_list.html",
                context,
                request=request,
            )
            return JsonResponse(data)
        else:
            context = dict(company_cost_category=cost_category)
            data["html_form"] = render_to_string(
                "company_cost_category/company_cost_category_delete.html",
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
                    if perm.codename == "cost_category_delete":
                        if request.method == "POST":
                            cost_category.delete()
                            data["form_is_valid"] = True
                            company_cost_category_list = (
                                CostCategory.objects.all().order_by("-id")
                            )
                            context = dict(
                                company_cost_category_list=company_cost_category_list
                            )
                            data["company_cost_category"] = render_to_string(
                                "company_cost_category/company_cost_category_list.html",
                                context,
                                request=request,
                            )
                            return JsonResponse(data)
                        else:
                            context = dict(company_cost_category=cost_category)
                            data["html_form"] = render_to_string(
                                "company_cost_category/company_cost_category_delete.html",
                                context,
                                request=request,
                            )
                            return JsonResponse(data)

            data["html_form"] = render_to_string(
                "errors/403-contents.html", {}, request=request
            )
            return JsonResponse(data)
