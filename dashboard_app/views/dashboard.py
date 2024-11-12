import json

from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from agent_management_app.models import AgentInfo, AgentTransaction
from passenger_app.models import Passenger
from passenger_app.models import PassengerDocument


MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}


def monthly_income(year, month_name):
    month = MONTHS.get(month_name)
    if not month:
        raise ValueError("Invalid month name")

    total_credit = (
        AgentTransaction.objects.filter(
            created_date__year=year, created_date__month=month
        ).aggregate(Sum("credit"))["credit__sum"]
        or 0
    )
    total_debit = (
        AgentTransaction.objects.filter(
            created_date__year=year, created_date__month=month
        ).aggregate(Sum("debit"))["debit__sum"]
        or 0
    )
    monthly_income = total_credit - total_debit
    return monthly_income


def calculate_total_income():
    total_credit = AgentTransaction.objects.aggregate(Sum("credit"))["credit__sum"] or 0
    total_debit = AgentTransaction.objects.aggregate(Sum("debit"))["debit__sum"] or 0
    agents_total_income = total_credit - total_debit
    return agents_total_income


def calculate_current_year_income():
    current_year = timezone.now().year
    total_credit = (
        AgentTransaction.objects.filter(created_date__year=current_year).aggregate(
            Sum("credit")
        )["credit__sum"]
        or 0
    )
    total_debit = (
        AgentTransaction.objects.filter(created_date__year=current_year).aggregate(
            Sum("debit")
        )["debit__sum"]
        or 0
    )
    current_year_income = total_credit - total_debit
    return current_year_income


def calculate_current_month_income():
    current_year = timezone.now().year
    current_month = timezone.now().month
    total_credit = (
        AgentTransaction.objects.filter(
            created_date__year=current_year, created_date__month=current_month
        ).aggregate(Sum("credit"))["credit__sum"]
        or 0
    )
    total_debit = (
        AgentTransaction.objects.filter(
            created_date__year=current_year, created_date__month=current_month
        ).aggregate(Sum("debit"))["debit__sum"]
        or 0
    )
    current_month_income = total_credit - total_debit
    return current_month_income


@login_required
def hrm_index(request):
    passport_status = {
        "name": "Passport Received",
        "count": PassengerDocument.objects.filter(
            document_name="passport_received"
        ).count(),
        "bg_color": "#fac858",
    }

    police_clearance_status = {
        "name": "Police Clearance",
        "count": PassengerDocument.objects.filter(
            document_name="police_clearance"
        ).count(),
        "bg_color": "#ee6666",
    }

    medical_certificate_status = {
        "name": "Medical Certificate",
        "count": PassengerDocument.objects.filter(
            document_name="medical_certificate"
        ).count(),
        "bg_color": "#73c0de",
    }

    training_status = {
        "name": "Training Status",
        "count": PassengerDocument.objects.filter(
            document_name="training_status"
        ).count(),
        "bg_color": "#3ba272",
    }

    visa_status = {
        "name": "Visa Status",
        "count": PassengerDocument.objects.filter(document_name="visa_status").count(),
        "bg_color": "#fc8754",
    }

    mofa_status = {
        "name": "MOFA Status",
        "count": PassengerDocument.objects.filter(document_name="mofa_status").count(),
        "bg_color": "#a56cc1",
    }

    finger_appointment_status = {
        "name": "Finger Appointment",
        "count": PassengerDocument.objects.filter(
            document_name="finger_appointment"
        ).count(),
        "bg_color": "#f7a35c",
    }

    finger_status = {
        "name": "Finger Status",
        "count": PassengerDocument.objects.filter(
            document_name="finger_status"
        ).count(),
        "bg_color": "#7cb5ec",
    }

    manpower_status = {
        "name": "Manpower Status",
        "count": PassengerDocument.objects.filter(
            document_name="manpower_status"
        ).count(),
        "bg_color": "#90ed7d",
    }

    ticket_status = {
        "name": "Ticket Status",
        "count": PassengerDocument.objects.filter(
            document_name="ticket_status"
        ).count(),
        "bg_color": "#f45b5b",
    }

    fly_success_status = {
        "name": "Fly Success",
        "count": PassengerDocument.objects.filter(
            document_name="flight", passenger__fly_status=True
        ).count(),
        "bg_color": "#8085e9",
    }

    document_status_list = [
        passport_status,
        police_clearance_status,
        medical_certificate_status,
        training_status,
        visa_status,
        mofa_status,
        finger_appointment_status,
        finger_status,
        manpower_status,
        ticket_status,
        fly_success_status,
    ]

    barChart_data = [
        {
            2023: [
                monthly_income(2023, "January"),
                monthly_income(2023, "February"),
                monthly_income(2023, "March"),
                monthly_income(2023, "April"),
                monthly_income(2023, "May"),
                monthly_income(2023, "June"),
                monthly_income(2023, "July"),
                monthly_income(2023, "August"),
                monthly_income(2023, "September"),
                monthly_income(2023, "October"),
                monthly_income(2023, "November"),
                monthly_income(2023, "December"),
            ],
            2024: [
                monthly_income(2024, "January"),
                monthly_income(2024, "February"),
                monthly_income(2024, "March"),
                monthly_income(2024, "April"),
                monthly_income(2024, "May"),
                monthly_income(2024, "June"),
                monthly_income(2024, "July"),
                monthly_income(2024, "August"),
                monthly_income(2024, "September"),
                monthly_income(2024, "October"),
                monthly_income(2024, "November"),
                monthly_income(2024, "December"),
            ],
            2025: [
                monthly_income(2025, "January"),
                monthly_income(2025, "February"),
                monthly_income(2025, "March"),
                monthly_income(2025, "April"),
                monthly_income(2025, "May"),
                monthly_income(2025, "June"),
                monthly_income(2025, "July"),
                monthly_income(2025, "August"),
                monthly_income(2025, "September"),
                monthly_income(2025, "October"),
                monthly_income(2025, "November"),
                monthly_income(2025, "December"),
            ],
        }
    ]

    data = [
        {
            "value": status["count"],
            "name": status["name"],
            "itemStyle": {"color": status["bg_color"]},
        }
        for status in document_status_list
    ]

    context = {
        # Dynamic Styles
        "page_name": "Dashboard",
        "dashboard_nav_link_status": "active",
        # Human Count
        "agent_count": AgentInfo.objects.filter(status=True).count(),
        "passenger_ongoing_count": Passenger.objects.filter(
            fly_status=False,
            cancel_status=False,
            money_refund_status=False,
            status=True,
        ).count(),
        "passenger_successful_count": Passenger.objects.filter(
            fly_status=True,
            cancel_status=False,
            money_refund_status=False,
            status=True,
        ).count(),
        # Document Count
        "document_status_list": document_status_list,
        # Pie Chart Data
        "data_json": json.dumps(data),  # Serialize the data to JSON
        # Bar Chart Data
        "barChart_data": json.dumps(barChart_data),
        # Total Income
        "agents_total_income": calculate_total_income(),
        "agents_current_year_income": calculate_current_year_income(),
        "agents_current_month_income": calculate_current_month_income(),
    }

    return render(request, "dashboard/dashboard.html", context)


@login_required
def hrm_notifications(request):
    return render(request, "dashboard/notifications.html")
