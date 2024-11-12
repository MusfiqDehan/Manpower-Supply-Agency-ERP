from django.db import models

from agent_management_app.models import AgentInfo
from passenger_app.models import Passenger


class Notification(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    agent = models.ForeignKey(
        AgentInfo,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="agent_notifications",
    )
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="passenger_notifications",
    )
    is_read = models.BooleanField(default=False)
    expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
