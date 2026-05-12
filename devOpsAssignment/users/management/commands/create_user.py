import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    """Emergency user creator"""

    envvars = {
        "unames": "TICKETSYSTEM_USERNAME",
        "pwds": "TICKETSYSTEM_PASSWORD",
        "emails": "TICKETSYSTEM_EMAIL",
        "roles": "TICKETSYSTEM_ROLE",
        "fnames": "TICKETSYSTEM_FIRST_NAME",
        "lnames": "TICKETSYSTEM_LAST_NAME",
        "supeflags": "TICKETSYSTEM_SUPE_FLAG",
    }

    def handle(self, *args, **opts):
        User = get_user_model()
        unames = os.environ.get(self.envvars["unames"]).split(";")
        pwds = os.environ.get(self.envvars["pwds"]).split(";")
        emails = os.environ.get(self.envvars["emails"]).split(";")
        roles = os.environ.get(self.envvars["roles"]).split(";")
        fnames = os.environ.get(self.envvars["fnames"]).split(";")
        lnames = os.environ.get(self.envvars["lnames"]).split(";")
        supeflags = os.environ.get(self.envvars["supeflags"]).split(";")

        user_list = zip([unames, pwds, emails, roles, fnames, lnames, supeflags])

        for uname, pwd, email, role, fname, lname, supeflag in user_list:
            with transaction.atomic():
                user, created = User.objects.get_or_create(username=uname)

                if not created:
                    self.stdout.write(
                        self.style.WARNING(f"User '{uname}' already exists; skipping. ")
                    )
                    return

                user.email = email
                user.first_name = fname
                user.last_name = lname
                user.role = role
                if supeflag == "true":
                    user.is_staff = True
                    user.is_superuser = True
                user.set_password(pwd)
                user.save()

            self.stdout.write(self.style.SUCCESS(f"{role} '{uname}' created"))
