import uuid
from django.db import models
from django.contrib.auth.models import User


class MobilityStateRecord(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mobility_state')
    state = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MobilityState for {self.user.username}"


class SavedEstimate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='estimates')
    name = models.CharField(max_length=255)
    state = models.JSONField(default=dict)
    total_cost = models.FloatField(default=0)
    currency = models.CharField(max_length=10, default='USD')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.name} ({self.currency} {self.total_cost:,.0f})"
