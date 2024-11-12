from django.urls import path

from company_cost_app.views import company_cost, cost_category

app_name = "company_cost_app"

urlpatterns = [
    path("company_cost/", company_cost.company_cost, name="company_cost"),
    path(
        "company_cost/create",
        company_cost.company_cost_create,
        name="company_cost_create",
    ),
    path(
        "company_cost/edit/<pk>",
        company_cost.company_cost_edit,
        name="company_cost_edit",
    ),
    path(
        "company_cost/delete/<pk>",
        company_cost.company_cost_delete,
        name="company_cost_delete",
    ),
    # New path for filtering by category
    path(
        "company_cost/filter_by_category",
        company_cost.filter_by_category,
        name="filter_by_category",
    ),
    path(
        "company_cost/filter_by_date/",
        company_cost.filter_by_date,
        name="filter_by_date",
    ),
    path(
        "company_cost/export/",
        company_cost.export_company_cost,
        name="export_company_cost",
    ),
    # cost category
    path(
        "company_cost_category/",
        cost_category.company_cost_category,
        name="company_cost_category",
    ),
    path(
        "company_cost_category/create",
        cost_category.company_cost_category_create,
        name="company_cost_category_create",
    ),
    path(
        "company_cost_category/edit/<pk>",
        cost_category.company_cost_category_edit,
        name="company_cost_category_edit",
    ),
    path(
        "company_cost_category/delete/<pk>",
        cost_category.company_cost_category_delete,
        name="company_cost_category_delete",
    ),
    #     path(
    #         "company_cost_category/view/<pk>",
    #         cost_category.company_cost_category_view,
    #         name="company_cost_category_view",
    #     ),
]
