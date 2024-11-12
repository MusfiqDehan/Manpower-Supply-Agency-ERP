from django.urls import path
from .views import (
    dashboard,
    notifications,
)
# from dashboard_app.context_processors import (
#     mark_as_read,
#     delete_notification,
#     mark_all_as_read,
# )

app_name = "dashboard_app"

urlpatterns = [
    # Root HRM Home Dashboard
    path("home/", dashboard.hrm_index, name="dashboard"),  # default page index.
    # notifications page.
    path("notifications/", notifications.show_notifications, name="notifications"),
    path(
        "notifications/mark-as-read/<int:notification_id>/",
        notifications.mark_as_read,
        name="mark_as_read",
    ),
    path(
        "notifications/delete/<int:notification_id>/",
        notifications.delete_notification,
        name="delete_notification",
    ),
    path(
        "notifications/mark-all-as-read/",
        notifications.mark_all_as_read,
        name="mark_all_as_read",
    ),
    path(
        "notifications/action/<int:notification_id>/",
        notifications.notification_action,
        name="notification_action",
    ),
    path(
        "notifications/create/",
        notifications.create_notification,
        name="create_notification",
    ),
]
