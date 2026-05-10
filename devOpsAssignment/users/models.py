from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "user", "User"
        MANAGER = "manager", "Manager"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        help_text="How much access a user has self or everyone.",
    )

    @property
    def is_manager(self) -> bool:
        return self.role == self.Role.MANAGER

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"
