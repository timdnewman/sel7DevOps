from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    """Based on the standard user with Role added
    Users can raise and view their own tickets
    Managers can also view anyones ticket and update the status    
    """
    class Role(models.TextChoices):
        USER = "user", "User"
        MANAGER = "manager", "Manager"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        help_text="Role - for security basis",
    )

    @property
    def is_manager(self) -> bool:
        return self.role == self.Role.MANAGER

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"