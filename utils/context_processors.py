from dashboard_app.models import Notification


def notifications_processor(request):
    notifications = Notification.objects.all().order_by("-id")[:20]

    unread_notifications_count = Notification.objects.filter(is_read=False).count()

    # Display "99+" if unread notifications are more than 100
    unread_notifications = (
        "99+" if unread_notifications_count > 100 else unread_notifications_count
    )
    return {
        "notifications": notifications,
        "unread_notifications": unread_notifications,
    }
