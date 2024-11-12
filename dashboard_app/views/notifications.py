from datetime import datetime, timedelta

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from agent_management_app.models import AgentDocument
from passenger_app.models import PassengerDocument
from dashboard_app.models import Notification


@login_required
def show_notifications(request):
    notifications = Notification.objects.all().order_by("-id")
    paginator = Paginator(notifications, 50)  # Show 50 items per page

    page_number = request.GET.get("page")
    notifications_pages = paginator.get_page(page_number)
    context = {
        "page_name": "Notifications",
        "notifications_pages": notifications_pages,
    }

    return render(request, "notification/notifications.html", context)


@require_POST
@csrf_exempt
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    return JsonResponse({"success": True, "unread_notifications": unread_notifications})


@require_POST
@csrf_exempt
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    return JsonResponse({"success": True, "unread_notifications": unread_notifications})


@require_POST
@csrf_exempt
def mark_all_as_read(request):
    Notification.objects.filter(is_read=False).update(is_read=True)
    unread_notifications = Notification.objects.filter(is_read=False).count()
    return JsonResponse({"success": True, "unread_notifications": unread_notifications})


@require_POST
@csrf_exempt
def notification_action(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    if notification.agent:
        redirect_url = f"/agent/agent_details/{notification.agent.id}/"
    elif notification.passenger:
        redirect_url = f"/passenger/passenger_details/{notification.passenger.id}/"
    else:
        redirect_url = "/erp/notifications/"

    return JsonResponse({"success": True, "redirect_url": redirect_url})


def create_notification(request):
    passenger_documents = PassengerDocument.objects.all()
    agent_documents = AgentDocument.objects.all()

    current_date = datetime.now().date()

    # Check for passenger documents
    for document_passenger in passenger_documents:
        try:
            days_ago = document_passenger.expiry_date - timedelta(days=15)
            if str(current_date) == str(days_ago):
                Notification.objects.create(
                    name=f"{document_passenger.document_name.replace('_', ' ').title()} will expire soon",
                    description=f"Passenger Mr {document_passenger.passenger.full_name}'s {document_passenger.document_name} will expire on {document_passenger.expiry_date}",
                    passenger=document_passenger.passenger,
                    is_read=False,
                )
        except Exception as e:
            print(e)
            pass

    # Check for agent documents
    for document_agent in agent_documents:
        try:
            days_ago = document_agent.expiry_date - timedelta(days=15)

            if str(current_date) == str(days_ago):
                Notification.objects.create(
                    name=f"{document_agent.document_name} will expire soon",
                    description=f"Agent Mr {document_agent.agent.full_name}'s {document_agent.document_name} will expire on {document_agent.expiry_date}",
                    agent=document_agent.agent,
                    is_read=False,
                )
        except Exception as e:
            print(e)
            pass

    return HttpResponse("Success")
