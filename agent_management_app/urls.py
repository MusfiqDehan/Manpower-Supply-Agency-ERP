from django.urls import path
from agent_management_app.views import (
    agent,
    agent_details,
    agent_documents,
    agent_search,
    agent_account,
)


app_name = "agent_management_app"

urlpatterns = [
    # Agent management
    path("agent_view/", agent.agent_view, name="agent_view"),
    path("agent/add/", agent.agent_add, name="agent_add"),
    path("agent/<pk>/edit/", agent.agent_edit, name="agent_edit"),
    path("agent/<pk>/delete/", agent.agent_delete, name="agent_delete"),
    # agent details
    path("agent_details/<pk>/", agent_details.agent_details, name="agent_details"),
    # attendance report pagination
    path(
        "agent_details/pagination_index/<index>/<agent>",
        agent_details.pagination_index,
        name="pagination_index",
    ),
    path(
        "agent_details/pagination/<page_number>/<index>/<agent>/",
        agent_details.list_pagination,
        name="list_pagination",
    ),
    # agent search
    path("agent/search/", agent_search.agent_search, name="agent_search"),
    # agent account delete
    path(
        "agent_account_delete/<int:pk>/",
        agent_account.agent_account_delete,
        name="agent_account_delete",
    ),
    # Document
    path(
        "document/add/<agent_id>/",
        agent_documents.agent_document_add,
        name="agent_document_add",
    ),
    path(
        "document/<pk>/edit/",
        agent_documents.agent_document_edit,
        name="agent_document_edit",
    ),
    path(
        "document/<pk>/delete/",
        agent_documents.agent_document_delete,
        name="agent_document_delete",
    ),
    # passenger list
    path(
        "agent/passenger/<pk>/", agent_details.agent_passenger, name="agent_passenger"
    ),
    # ====================== Agent Account Management ============= --(RM)
    # Agent Account Crete/add.
    path(
        "account/add/<pk>/", agent_account.agent_account_add, name="agent_account_add"
    ),
    # Agent Transaction (Credit/Received).
    path(
        "receive/<pk>/",
        agent_account.agent_payment_receive,
        name="agent_payment_receive",
    ),
    # Agent Account (Debit/payment).
    path(
        "payment/<pk>/", agent_account.agent_payment_debit, name="agent_payment_debit"
    ),
    # Transaction Deleted.
    # Hold Transaction Edit
    path(
        "transaction/<pk>/edit",
        agent_account.agent_account_transaction_edit,
        name="agent_A_transaction_edit",
    ),
    # Agent Transaction deleted.
    path(
        "transaction/<pk>/delete/",
        agent_account.agent_transaction_delete,
        name="agent_transaction_delete",
    ),
    # agent transaction print
    path(
        "agent_transaction_print/",
        agent_account.agent_transaction_print,
        name="agent_transaction_print",
    ),
]
