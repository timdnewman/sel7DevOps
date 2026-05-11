from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
import json


class Ticket(models.Model):

    class Area(models.TextChoices):
        ENGINEERING = "engineering", "Engineering"
        TECHNOLOGY = "technology", "Technology"
        OPS = "ops", "Ops"
        STRATEGY = "strategy", "Strategy"
        SUPPORT = "support", "Support" 
    
    class Severity(models.TextChoices):
        ABLE = "able", "Able to work"
        PARTIAL = "partial", "Partially able to work"
        NOT_ABLE = "not_able", "Not able to work"

    class Status(models.TextChoices):
        OPENED = "opened", "Opened"
        ASSIGNED = "assigned", "Assigned"
        WORKING = "working", "Working"
        CLOSED = "closed", "Closed"
    
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2)],
        help_text="Name of the person raising the ticket.",
        )
    area = models.CharField(max_length=20, choices=Area.choices)
    severity = models.CharField(max_length=20, choices=Severity.choices)
    description = models.TextField(
            validators=[MinLengthValidator(10)],
            help_text="Describe the problem in at least 10 characters.",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPENED,
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets",
        help_text="The account that submitted this ticket (used for ownership checks).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["submitted_by", "-created_at"]),
        ]

    def __str__(self) -> str:
        return f"#{self.pk} — {self.name} ({self.get_status_display()})"

    def get_absolute_url(self) -> str:
        return reverse("tickets:detail", kwargs={"pk": self.pk})