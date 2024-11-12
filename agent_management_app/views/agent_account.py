import uuid
import openpyxl

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from agent_management_app.views import agent
from passenger_app.models import Passenger, PassengerDocument, PassengerTransaction
from agent_management_app.models import (
    AgentInfo,
    AgentAccount,
    AgentTransaction,
    AgentDocument,
)
from passenger_app.models import Passenger, PassengerDocument, PassengerTransaction
from company_cost_app.models import CompanyCost
from agent_management_app.forms import (
    AgentAccountForm,
    AgentTransactionForm,
    AgentAccuntTransactionEditForm,
    AgentTransactionEditForm,
)


# Agent Account Create.
@login_required
def agent_account_add(request, pk):
    data = dict()
    # data["source"] = "agent_account_add"

    print("Agent Account Add")

    agent = None
    agent_total_amount = None

    agent_account = None

    try:
        agent = get_object_or_404(AgentInfo, id=pk)
        agent_id = agent.id  # Agent ID

    except Http404:
        pass

    if request.method == "POST":
        form = AgentAccountForm(request.POST, request.FILES)

        if form.is_valid():
            selected_payment_type = request.POST.get("is_credit")

            instance = form.save(commit=False)

            if selected_payment_type == "True":  ##credit
                instance.total_balance = (
                    instance.total_balance - instance.opening_balance
                )

            else:  # debit
                instance.total_balance = (
                    instance.total_balance + instance.opening_balance
                )

            instance.save()
            data["form_is_valid"] = True
            data["agent_account_add"] = True

            # Agent account
            agent_account = AgentAccount.objects.get(agent=agent)

            data["agent_account_button"] = render_to_string(
                "agent_management/agent_account/agent_tabs_account_button.html",
                {
                    "agent_account": agent_account,
                    "user": request.user,
                },
            )

            data["agent_account"] = render_to_string(
                "agent_management/agent_account/agent_account_info.html",
                {
                    "agent_account": agent_account,
                    "user": request.user,
                },
            )

            data["agent_account_total_due"] = render_to_string(
                "agent_management/agent_account/agent_total_due_account.html",
                {
                    "agent_account": agent_account,
                    "user": request.user,
                },
            )

            return JsonResponse(data)

        else:
            data["form_is_valid"] = False
            return JsonResponse(data)

    else:
        form = AgentAccountForm()  # GET request

        context = {
            "form": form,
            "agent_id": pk,
            "user": request.user,
        }

        data["html_form"] = render_to_string(
            "agent_management/agent_account/agent_account_create.html",
            context,
            request=request,
        )

        return JsonResponse(data)


# Agent Account Delete
@csrf_exempt
@login_required
def agent_account_delete(request, pk):
    data = dict()

    agent_account = get_object_or_404(AgentAccount, id=pk)
    agent_id = agent_account.agent.id

    agent = get_object_or_404(AgentInfo, id=agent_id)

    if request.method == "POST":
        temp_agent_account = AgentAccount.objects.get(id=pk)
        temp_agent_account.delete()

        data["success"] = True

        data["agent_account_create_button"] = render_to_string(
            "agent_management/agent_account/agent_account_create_button.html",
            {
                "agent_details": agent,
                "user": request.user,
            },
            request=request,
        )

        return JsonResponse(data)

    else:
        context = {
            "agent_account": agent_account,
            "agent": agent,
            "agent_id": agent_id,
            "user": request.user,
        }

        data["html_form"] = render_to_string(
            "agent_management/agent_account/agent_account_delete_modal.html",
            context,
            request=request,
        )
        return JsonResponse(data)


# Agent Account Payment Received (Credit).
@login_required
def agent_payment_receive(request, pk):
    data = {}
    agent_account = AgentAccount.objects.get(id=pk)  # Agent Transaction

    agent_id = agent_account.agent.id  # Agent ID
    agent_details = get_object_or_404(AgentInfo, id=agent_id)  # Agent Account
    Agent_passenger_list = Passenger.objects.filter(
        agent_list=agent_details
    )  # Agent Passengers

    if request.method == "POST":
        form = AgentTransactionForm(request.POST, request.FILES)

        # Get the debit or credit amount
        credit_amount = request.POST.get("credit")
        agent_transaction_date = request.POST.get("payment_date")
        credit_amount = float(credit_amount)

        # Generate a unique transaction ID using UUID
        transaction_id = uuid.uuid4().hex[:20]  # Generate a 20-character unique ID

        # Get the passenger data from the form as lists
        selected_passenger_ids = request.POST.get("selected_passenger_data[]")

        # only Selected passenger will get the received amount .
        if selected_passenger_ids:
            selected_passenger_ids = request.POST.getlist("selected_passenger_data[]")
            selected_passenger_receive_amounts = request.POST.getlist(
                "passenger_amount_data[]"
            )
            selected_passenger_payment_notes = request.POST.getlist(
                "passenger_payment_note[]"
            )

            # Create a PassengerTransaction for each passenger
            for passenger_id, receive_amount, payment_note in zip(
                selected_passenger_ids,
                selected_passenger_receive_amounts,
                selected_passenger_payment_notes,
            ):
                try:
                    # Get the Passenger object
                    is_passenger = Passenger.objects.get(id=passenger_id)

                    # Create a PassengerTransaction
                    PassengerTransaction.objects.create(
                        passenger=is_passenger,
                        credit=receive_amount,
                        payment_transaction_id=transaction_id,
                        note=payment_note,
                        transaction_date=agent_transaction_date,
                    )
                    # You can add any additional logic here, if needed

                except Passenger.DoesNotExist:
                    # Handle the case where the Passenger doesn't exist
                    pass

        # If Not assign any Passenger then the amount will be divided all  passenger.
        else:
            # ======================= will be hold =========================================
            pass

        if form.is_valid():
            instance = form.save(commit=False)

            # Generate a unique transaction ID using UUID
            instance.payment_transaction_id = (
                transaction_id  # Generate a 20-character unique ID
            )

            instance.balance = (
                agent_account.total_balance + instance.credit
            ) - instance.debit

            # If Not Selected Any Passenger.
            if selected_passenger_ids:
                pass
            else:
                instance.transaction_hold_status = True

            instance.save()

            # Agent Total Amount
            agent_account.total_balance = instance.balance
            agent_account.save()

            data["form_is_valid"] = True
            data["agent_payment_receive"] = True

            # agent_account_payment_receive
            agent_account_payment_receive = AgentTransaction.objects.filter(
                agent_account__id=pk
            ).order_by("payment_date", "id")

            l = list(agent_account_payment_receive)
            for i in range(0, len(l)):
                if i == 0:
                    obj = l[i]

                    if agent_account.is_credit:
                        obj.balance = (
                            obj.credit - obj.debit
                        ) - agent_account.opening_balance
                    else:
                        obj.balance = (
                            obj.credit - obj.debit
                        ) + agent_account.opening_balance

                    obj.save()
                    agent_account.total_balance = obj.balance
                else:
                    p_obj = l[i - 1]
                    p_balance = p_obj.balance
                    obj = l[i]

                    obj.balance = p_balance + obj.credit - obj.debit
                    obj.save()
                    agent_account.total_balance = obj.balance

            print("agent_account_payment_receive", agent_account_payment_receive)
            data["receive_list"] = render_to_string(
                "agent_management/agent_account/agent_account_list.html",
                {
                    "receive_list": agent_account_payment_receive,
                    "user": request.user,
                },
            )

            agent_account_update = AgentAccount.objects.get(id=pk)  # Agent Account

            data["middleman_account"] = render_to_string(
                "agent_management/agent_account/agent_account_info.html",
                {
                    "agent_account": agent_account_update,
                    "user": request.user,
                },
            )

            data["middleman_account_total_due"] = render_to_string(
                "agent_management/agent_account/agent_total_due_account.html",
                {
                    "agent_account": agent_account_update,
                    "user": request.user,
                },
            )

            data["agent_total_balance"] = agent_account.total_balance

            return JsonResponse(data)

    else:
        form = AgentTransactionForm()  # GET request

    context = {
        "form": form,
        "middleman_id": pk,
        "agent_account_id": pk,
        "user": request.user,
        "middleman_passenger_list": Agent_passenger_list,
    }

    data["html_form"] = render_to_string(
        "agent_management/agent_account/agent_account_payment_receive.html",
        context,
        request=request,
    )
    return JsonResponse(data)


# Agent Account Payment Debit.
@login_required
def agent_payment_debit(request, pk):
    print("Agent Payment Debit 2222")
    agent_account = AgentAccount.objects.get(id=pk)  # Agent Transaction
    agent_id = agent_account.agent.id  # Agent ID

    agent_details = get_object_or_404(AgentInfo, id=agent_id)  # Agent Account

    Agent_passenger_list = Passenger.objects.filter(
        agent_list=agent_details
    )  # Agent Passengers

    data = {}
    data["source"] = "agent_payment_debit"
    if request.method == "POST":
        form = AgentTransactionForm(request.POST, request.FILES)
        # Get the debit or credit amount
        debit_amount = request.POST.get("debit")
        debit_amount = float(debit_amount)
        agent_transaction_date = request.POST.get("payment_date")

        # Get the passenger data from the form as lists
        selected_passenger_ids = request.POST.get("selected_passenger_data[]")

        # Generate a unique transaction ID using UUID
        transaction_id = uuid.uuid4().hex[:20]  # Generate a 20-character unique ID

        # only Selected passenger will get the received amount .
        if selected_passenger_ids:
            selected_passenger_ids = request.POST.getlist("selected_passenger_data[]")

            selected_passenger_receive_amounts = request.POST.getlist(
                "passenger_amount_data[]"
            )

            selected_passenger_payment_notes = request.POST.getlist(
                "passenger_payment_note[]"
            )

            # Create a PassengerTransaction for each passenger
            for passenger_id, receive_amount, payment_note in zip(
                selected_passenger_ids,
                selected_passenger_receive_amounts,
                selected_passenger_payment_notes,
            ):
                try:
                    # Get the Passenger object
                    is_passenger = Passenger.objects.get(id=passenger_id)

                    # Create a PassengerTransaction
                    PassengerTransaction.objects.create(
                        passenger=is_passenger,
                        debit=receive_amount,
                        payment_transaction_id=transaction_id,
                        note=payment_note,
                        transaction_date=agent_transaction_date,
                    )

                    CompanyCost.objects.create(
                        date_incurred=agent_transaction_date,
                        amount=receive_amount,
                        note=f"Debit transaction for passenger {is_passenger.full_name} by agent {agent_details.full_name}",
                    )
                    # You can add any additional logic here, if needed

                except Passenger.DoesNotExist:
                    # Handle the case where the Passenger doesn't exist
                    pass

        # If Not assign any Passenger then the debit amount will be divided all  passenger.
        else:
            pass

        if form.is_valid():
            instance = form.save(commit=False)

            # If Not Selected Any Passenger.
            if selected_passenger_ids:
                pass
            else:
                instance.transaction_hold_status = True

            # Generate a unique transaction ID using UUID
            instance.payment_transaction_id = (
                transaction_id  # Generate a 20-character unique ID
            )

            instance.balance = (
                agent_account.total_balance - instance.debit
            ) + instance.credit
            instance.save()

            agent_account.total_balance = instance.balance
            agent_account.save()

            data["form_is_valid"] = True
            data["agent_payment_debit"] = True

            # Agent Account Transaction
            agent_account_payment_receive = AgentTransaction.objects.filter(
                agent_account__id=pk
            ).order_by("payment_date", "id")

            l = list(agent_account_payment_receive)
            for i in range(0, len(l)):
                if i == 0:
                    obj = l[i]

                    if agent_account.is_credit:
                        obj.balance = (
                            obj.credit - obj.debit
                        ) - agent_account.opening_balance
                    else:
                        obj.balance = (
                            obj.credit - obj.debit
                        ) + agent_account.opening_balance

                    obj.save()
                    agent_account.total_balance = obj.balance
                else:
                    p_obj = l[i - 1]
                    p_balance = p_obj.balance
                    obj = l[i]

                    obj.balance = p_balance + obj.credit - obj.debit
                    obj.save()
                    agent_account.total_balance = obj.balance

            data["receive_list"] = render_to_string(
                "agent_management/agent_account/agent_account_list.html",
                {
                    "receive_list": agent_account_payment_receive,
                    "user": request.user,
                },
            )

            # Agent Update Account
            agent_account_update = AgentAccount.objects.get(id=pk)  # Agent Account

            data["middleman_account"] = render_to_string(
                "agent_management/agent_account/agent_account_info.html",
                {
                    "agent_account": agent_account_update,
                    "user": request.user,
                },
            )

            data["middleman_account_total_due"] = render_to_string(
                "agent_management/agent_account/agent_total_due_account.html",
                {
                    "agent_account": agent_account_update,
                    "user": request.user,
                },
            )

            data["agent_total_balance"] = agent_account.total_balance

            return JsonResponse(data)

    else:
        form = AgentTransactionForm()  # GET request

    context = {
        "form": form,
        "middleman_id": pk,
        "agent_account_id": pk,
        "user": request.user,
        "middleman_passenger_list": Agent_passenger_list,
    }

    data["html_form"] = render_to_string(
        "agent_management/agent_account/agent_account_payment_debit.html",
        context,
        request=request,
    )
    return JsonResponse(data)


# Agent Transaction Edit ============
@login_required
def agent_account_transaction_edit(request, pk):
    data = {}
    agent_transaction = get_object_or_404(AgentTransaction, id=pk)
    agent_transaction_id = agent_transaction.id

    agent_account_id = agent_transaction.agent_account.id

    # agent Account
    agent_account = AgentAccount.objects.get(id=agent_account_id)

    # Agent Passenger List
    agent_id = agent_account.agent.id
    agent_details = get_object_or_404(AgentInfo, id=agent_id)
    agent_passenger_list = Passenger.objects.filter(agent_list=agent_details)

    # when POST
    if request.method == "POST":
        form = AgentTransactionEditForm(
            request.POST, request.FILES, instance=agent_transaction
        )

        # Get the passenger data from the form as lists
        selected_passenger_ids = request.POST.get("selected_passenger_data[]")

        # only Selected passenger will get the received amount .
        if selected_passenger_ids:
            selected_passenger_ids = request.POST.getlist("selected_passenger_data[]")
            selected_passenger_receive_amounts = request.POST.getlist(
                "passenger_amount_data[]"
            )
            selected_passenger_payment_notes = request.POST.getlist(
                "passenger_payment_note[]"
            )

            # Create a PassengerTransaction for each passenger
            for passenger_id, receive_amount, payment_note in zip(
                selected_passenger_ids,
                selected_passenger_receive_amounts,
                selected_passenger_payment_notes,
            ):
                try:
                    # Get the Passenger object
                    is_passenger = Passenger.objects.get(id=passenger_id)

                    if agent_transaction.credit != 0.0:
                        # Create a PassengerTransaction
                        PassengerTransaction.objects.create(
                            passenger=is_passenger,
                            credit=receive_amount,
                            payment_transaction_id=agent_transaction.payment_transaction_id,
                            note=payment_note,
                        )

                    else:
                        # Create a PassengerTransaction
                        PassengerTransaction.objects.create(
                            passenger=is_passenger,
                            debit=receive_amount,
                            payment_transaction_id=agent_transaction.payment_transaction_id,
                            note=payment_note,
                        )

                except Passenger.DoesNotExist:
                    # Handle the case where the Passenger doesn't exist
                    pass

        # If Not assign any Passenger then the amount will be divided all  passenger.
        else:
            # ======================= will be hold =========================================
            pass

        # MiddlemanAccount Transaction.
        if form.is_valid():
            if selected_passenger_ids:
                agent_transaction.transaction_hold_status = False
            else:
                agent_transaction.transaction_hold_status = True

            agent_transaction.save()

            data["form_is_valid"] = True
            data["agent_account_transaction_edit"] = True

            agent_account2 = AgentAccount.objects.get(id=agent_account_id)
            agentID = agent_account2.id

            agent_account_payment_receive = AgentTransaction.objects.filter(
                agent_account__id=agentID
            ).order_by("payment_date", "id")

            data["receive_list"] = render_to_string(
                "agent_management/agent_account/agent_account_list.html",
                {
                    "receive_list": agent_account_payment_receive,
                    "user": request.user,
                },
            )

            data["middleman_account"] = render_to_string(
                "agent_management/agent_account/agent_account_info.html",
                {
                    "agent_account": agent_account2,
                    "user": request.user,
                },
            )

            data["middleman_account_total_due"] = render_to_string(
                "agent_management/agent_account/agent_total_due_account.html",
                {
                    "agent_account": agent_account2,
                    "user": request.user,
                },
            )
            data["transaction_hold_status"] = agent_transaction.transaction_hold_status

            return JsonResponse(data)

    else:
        form = AgentTransactionEditForm(instance=agent_transaction)  # GET request

    context = {
        "form": form,
        "user": request.user,
        "middleman_passenger_list": agent_passenger_list,
        "middleman_transaction": agent_transaction,
        "middleman_transaction_id": agent_transaction_id,
        "middleman_account": agent_account,
        "middleman_account_id": agent_account_id,
        "user": request.user,
    }

    data["transaction_hold_status"] = agent_transaction.transaction_hold_status

    data["html_form"] = render_to_string(
        "agent_management/agent_account/agent_transaction_edit.html",
        context,
        request=request,
    )
    return JsonResponse(data)


# Agent Transaction Delete
@login_required
def agent_transaction_delete(request, pk):
    data = {}

    agent_transaction = get_object_or_404(AgentTransaction, id=pk)
    agent_account_id = agent_transaction.agent_account.id
    agent_account = AgentAccount.objects.get(id=agent_account_id)
    agent_id = agent_account.agent.id
    agent_details = get_object_or_404(AgentInfo, id=agent_id)
    agent_passenger_list = Passenger.objects.filter(agent_list=agent_details)

    # Agent Account
    agent_account = AgentAccount.objects.get(id=agent_account_id)

    if request.method == "POST":
        # Agent Transaction Id
        payment_transaction_id = agent_transaction.payment_transaction_id

        # Agent Passenger list filter with Transaction Id
        agent_passenger_transactions_list = PassengerTransaction.objects.filter(
            passenger__in=agent_passenger_list,
            payment_transaction_id=payment_transaction_id,
        )

        # Delete the Middleman Passenger Transactions
        agent_passenger_transactions_list.delete()

        # Delete the agent Transaction
        agent_transaction.delete()

        data["form_is_valid"] = True

        # Agent all Transactions List
        agent_account_payment_receive = AgentTransaction.objects.filter(
            agent_account__id=agent_account_id
        ).order_by("payment_date", "id")

        l = list(agent_account_payment_receive)
        for i in range(0, len(l)):
            if i == 0:
                obj = l[i]

                if agent_account.is_credit:
                    obj.balance = (
                        obj.credit - obj.debit
                    ) - agent_account.opening_balance
                else:
                    obj.balance = (
                        obj.credit - obj.debit
                    ) + agent_account.opening_balance

                obj.save()
                agent_account.total_balance = obj.balance
            else:
                p_obj = l[i - 1]
                p_balance = p_obj.balance
                obj = l[i]

                obj.balance = p_balance + obj.credit - obj.debit
                obj.save()

                agent_account.total_balance = obj.balance

        if agent_account_payment_receive:
            pass
        else:
            if agent_account.is_credit:
                agent_account.total_balance = -(agent_account.opening_balance)
            else:
                agent_account.total_balance = agent_account.opening_balance

        transaction_count = agent_account_payment_receive.count()
        data["agent_account_payment_receive"] = transaction_count

        # agent_account2 = MiddlemanAccount.objects.get(id=pk)
        agnet_account2 = AgentAccount.objects.get(id=agent_account_id)

        data["receive_list"] = render_to_string(
            "agent_management/agent_account/agent_account_list.html",
            {
                "receive_list": agent_account_payment_receive,
                "user": request.user,
            },
        )

        data["middleman_account"] = render_to_string(
            "agent_management/agent_account/agent_account_info.html",
            {
                "agent_account": agnet_account2,
                "user": request.user,
            },
        )

        data["middleman_account_total_due"] = render_to_string(
            "agent_management/agent_account/agent_total_due_account.html",
            {
                "agent_account": agnet_account2,
                "user": request.user,
            },
        )

        data["agent_total_balance"] = agent_account.total_balance

        return JsonResponse(data)

    else:
        context = {
            "middleman_transaction": agent_transaction,
            "middleman_account_id": agent_account_id,
            "user": request.user,
        }

        data["html_form"] = render_to_string(
            "agent_management/agent_account/agent_transaction_delete.html",
            context,
            request=request,
        )
        return JsonResponse(data)


def agent_transaction_print(request):
    data = dict()
    agent_pk = request.GET["agent_pk"]
    agent = AgentInfo.objects.get(pk=agent_pk)
    agent_transaction_list = AgentTransaction.objects.filter(
        agent_account=agent.agent_account
    )

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    data = [
        ["Date", "Payment Type", "Note", "Debit", "Credit", "Balance"],
    ]
    agent_transaction = [
        [
            agent_transaction.payment_date
            if agent_transaction.payment_date
            else agent_transaction.created_date,
            agent_transaction.payment_type if agent_transaction.payment_type else "",
            agent_transaction.note if agent_transaction.note else "",
            agent_transaction.debit,
            agent_transaction.credit,
            agent_transaction.balance,
        ]
        for agent_transaction in agent_transaction_list
    ]

    data.extend(agent_transaction)
    print(data, "--------------data-------------")
    for row in data:
        sheet.append(row)

    sheet.column_dimensions["A"].width = 20
    sheet.column_dimensions["B"].width = 20
    sheet.column_dimensions["C"].width = 30
    sheet.column_dimensions["D"].width = 20
    sheet.column_dimensions["E"].width = 20
    sheet.column_dimensions["F"].width = 20

    # Prepare the HTTP response to return the Excel file
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=agent_transaction.xlsx"
    workbook.save(response)

    return response
    # return JsonResponse(data,safe=False)
