from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    # Add the role field to the existing fieldsets rather than redefining them
    # so we keep all of Django's password / permission UI.
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = DjangoUserAdmin.list_filter + ("role",)