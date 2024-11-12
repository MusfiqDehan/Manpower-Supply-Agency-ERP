from django.shortcuts import render
from agent_management_app.forms import AgentInfoSubmitForm
from agent_management_app.models import (
    AgentInfo,
    AgentDocument,
    AgentAccount,
    AgentTransaction,
)
from passenger_app.models import Passenger, PassengerTransaction
from django.contrib.auth.decorators import login_required

from django.http import Http404
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.core.paginator import Paginator, PageNotAnInteger


@login_required
def agent_details(request, pk):
    user_groups = request.user.Group_Users.all()
    # passenger_transactions = PassengerTransaction.objects.all()

    # passenger_transactions.delete()

    # Default value
    agent_account_list = None
    agent_passenger_list = None

    # Agent details
    agent = AgentInfo.objects.get(id=pk)
    agent_account = AgentAccount.objects.filter(agent__id=pk).first()

    # Agent account
    try:
        agent_account_list = get_object_or_404(AgentAccount, agent__id=pk)
    except Http404:
        pass

    try:
        account_opening_value = AgentAccount.objects.filter(agent__id=pk).first()
        if account_opening_value is not None:
            agent_account_list_exclude_first = AgentAccount.objects.filter(
                agent__id=pk
            ).exclude(id=account_opening_value.id)
        else:
            agent_account_list_exclude_first = None
    except AgentAccount.DoesNotExist:
        account_opening_value = None
        agent_account_list_exclude_first = None

    # Agent document part
    agent_document_list = AgentDocument.objects.filter(agent__id=pk).order_by(
        "document_name"
    )

    agentTransaction_list = AgentTransaction.objects.filter(
        agent_account=agent_account
    ).order_by("payment_date", "id")

    l = list(agentTransaction_list)
    for i in range(0, len(l)):
        if i == 0:
            obj = l[i]

            if agent_account.is_credit:
                obj.balance = (obj.credit - obj.debit) - agent_account.opening_balance
            else:
                obj.balance = (obj.credit - obj.debit) + agent_account.opening_balance

            obj.save()
            agent_account.total_balance = obj.balance
        else:
            p_obj = l[i - 1]
            p_balance = p_obj.balance
            obj = l[i]

            obj.balance = p_balance + obj.credit - obj.debit
            obj.save()
            agent_account.total_balance = obj.balance

    agentTransaction_list_count = agentTransaction_list.count()

    try:
        agent_passenger_list = Passenger.objects.filter(agent_list=agent)
        agent_passengers_list_count = agent_passenger_list.count()
        # agent_passengers_list_count = float(agent_passengers_list_count)
    except Http404:
        pass

    context = {
        "page_name": "Agent Details",
        "agent_details_nav_link_status": "active",
        "agent": agent,
        "agent_details": agent,
        "agent_account": agent_account,
        "agent_document_list": agent_document_list,
        "agent_account_list": agent_account_list,
        "agent_account_list_exclude_first": agent_account_list_exclude_first,
        "account_opening_value": account_opening_value,
        "agent_id": agent.id,
        "agent_passenger_list": agent_passenger_list,
        "agent_passengers_list_count": agent_passengers_list_count,
        "user": request.user,
        "agentTransaction_list": agentTransaction_list,
        "agentTransaction_list_count": agentTransaction_list_count,
    }

    if request.user.is_superuser:
        return render(
            request, "agent_management/agent_details/agent_details.html", context
        )
    else:
        if user_groups is None:
            return render(request, "errors/403.html")
        else:
            for user_group in user_groups:
                group_permissions = user_group.permissions.all()
                for perm in group_permissions:
                    if perm.codename == "agent_profile_view":
                        return render(
                            request,
                            "agent_management/agent_details/agent_details.html",
                            context,
                        )
            return render(request, "errors/403.html")


##pagination
@login_required
def list_pagination(request, page_number, index, agent, search_string=None):
    agent = AgentInfo.objects.get(id=int(agent))
    index = index
    data = dict()
    search_string = request.GET.get("search_text", None)

    data_queryset = []
    if search_string is not None:
        data_queryset = AgentTransaction.objects.filter(
            agent_account=agent.agent_account
        ).order_by("payment_date", "id")

    else:
        data_queryset = AgentTransaction.objects.filter(
            agent_account=agent.agent_account
        ).order_by("payment_date", "id")

    items_per_page = 10
    paginator = Paginator(data_queryset, items_per_page)
    # page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_range = paginator.page_range
    total_pages = paginator.num_pages

    lists = list(page_range)
    chunk_size = 5
    chunks = []

    for i in range(0, total_pages, chunk_size):
        start = i
        end = i + chunk_size
        chunk = lists[start:end]
        chunks.append(chunk)

    chunk_length = len(chunks) - 1

    for chunk_number, chunk in enumerate(chunks):
        if int(page_number) in chunk:
            index = chunk_number

    data["html_save_user"] = render_to_string(
        "agent_management/agent_account/agent_account_list.html",
        {"page_obj": page_obj, "agent": agent},
        request=request,
    )

    context = {
        "page_obj": page_obj,
        "page_range": page_range,
        "total_pages": total_pages,
        "chunks": chunks[int(index)],
        "chunks_list": chunks,
        "index": int(index),
        "chunk_length": chunk_length,
        "agent": agent,
    }

    data["html_pagination"] = render_to_string(
        "agent_management/agent_account/agent_account_pagination.html",
        context,
        request=request,
    )
    return JsonResponse(data)


# Pagination (dot)
@login_required
def pagination_index(request, index, agent, search_string=None):
    data = dict()
    print(agent, "-----agent----")
    agent = AgentInfo.objects.get(id=int(agent))

    search_string = request.GET.get("search_text", None)

    data_queryset = AgentTransaction.objects.filter(
        agent_account=agent.agent_account
    ).order_by("payment_date", "id")

    items_per_page = 10

    paginator = Paginator(data_queryset, items_per_page)

    page_range = paginator.page_range
    total_pages = paginator.num_pages

    lists = list(page_range)
    chunk_size = 5
    chunks = []

    for i in range(0, total_pages, chunk_size):
        start = i
        end = i + chunk_size
        chunk = lists[start:end]
        chunks.append(chunk)

    chunk_length = len(chunks) - 1

    context = {
        "page_range": page_range,
        "total_pages": total_pages,
        "chunks": chunks[int(index)],
        "chunks_list": chunks,
        "index": int(index),
        "chunk_length": chunk_length,
        "agent": agent,
    }

    data["html_pagination"] = render_to_string(
        "agent_management/agent_account/agent_account_pagination.html",
        context,
        request=request,
    )

    return JsonResponse(data)


from django.shortcuts import get_object_or_404


@login_required
def agent_passenger(request, pk):
    # Get the AgentInfo object for the specified agent_id
    agent = AgentInfo.objects.get(id=pk)

    # Filter passengers based on the agent
    agent_passenger_list = Passenger.objects.filter(agent_list=agent).order_by("-id")

    context = {
        "agent_passenger_list": agent_passenger_list,
        "agent": agent,  # Pass the agent object to the template for reference
        "user": request.user,
    }

    return render(request, "agent_management/agent_details/agent_details.html", context)
