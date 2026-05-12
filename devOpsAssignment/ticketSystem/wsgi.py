"""
WSGI config for ticketSystem project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# if "WEBSITE_HOSTNAME" in os.environ:
#     settings_module = "ticketSystem.deployment"
# else:
#     settings_module = "ticketSystem.settings"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ticketSystem.settings")

application = get_wsgi_application()
