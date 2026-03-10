import uuid
from django.db import models
from django.contrib.auth.models import User

try:
    from pgvector.django import VectorField
    _VECTOR_AVAILABLE = True
except ImportError:
    _VECTOR_AVAILABLE = False

from .embeddings import EMBEDDING_DIM


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

    if _VECTOR_AVAILABLE:
        embedding = VectorField(dimensions=EMBEDDING_DIM, null=True, blank=True)
    else:
        embedding = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.name} ({self.currency} {self.total_cost:,.0f})"


class MarketInsightCache(models.Model):
    """Persistent vector-searchable cache for Gemini market insight responses."""
    country_code = models.CharField(max_length=10, db_index=True)
    city_code = models.CharField(max_length=10, db_index=True)
    city_label = models.CharField(max_length=200)
    currency = models.CharField(max_length=10, db_index=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    if _VECTOR_AVAILABLE:
        embedding = VectorField(dimensions=EMBEDDING_DIM, null=True)
    else:
        embedding = models.JSONField(null=True, blank=True)

    class Meta:
        unique_together = [('country_code', 'city_code', 'currency')]

    def __str__(self):
        return f"{self.city_label} ({self.currency})"
