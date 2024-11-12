from django.urls import path
from company_documentation_app.views import company_document, company_document_category


app_name = "company_documentation_app"

urlpatterns = [
    path("document/", company_document.document_list_view, name="index"),
    # CRUD
    path("create/", company_document.document_create, name="document_create"),
    path("edit/<pk>", company_document.document_edit, name="document_edit"),
    path("delete/<pk>", company_document.document_delete, name="document_delete"),
    # document category
    path(
        "company_document_category/",
        company_document_category.company_document_category,
        name="company_document_category",
    ),
    path(
        "company_document_category/create",
        company_document_category.company_document_category_create,
        name="company_document_category_create",
    ),
    path(
        "company_document_category/edit/<pk>",
        company_document_category.company_document_category_edit,
        name="company_document_category_edit",
    ),
    path(
        "company_document_category/delete/<pk>",
        company_document_category.company_document_category_delete,
        name="company_document_category_delete",
    ),
]
