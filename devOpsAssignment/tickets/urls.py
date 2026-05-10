from django.urls import path

from .views import (
    TicketCreateView,
    TicketDetailView,
    TicketListView,
    TicketStatusUpdateView,
)

app_name = "tickets"

urlpatterns = [
    path("", TicketListView.as_view(), name="list"),
    path("new/", TicketCreateView.as_view(), name="create"),
    path("<int:pk>/", TicketDetailView.as_view(), name="detail"),
    path("<int:pk>/status/", TicketStatusUpdateView.as_view(), name="status_update"),
]