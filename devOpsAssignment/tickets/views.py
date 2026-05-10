from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from .forms import StatusUpdateForm, TicketForm
from .models import Ticket


class ManagerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Restrict a view to authenticated managers."""

    def test_func(self) -> bool:
        return self.request.user.is_authenticated and self.request.user.is_manager

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 25

    def get_queryset(self):
        qs = Ticket.objects.select_related("submitted_by").all()
        user = self.request.user

        if not user.is_manager:
            return qs.filter(submitted_by=user)

        if self.request.GET.get("scope") == "mine":
            return qs.filter(submitted_by=user)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["scope"] = self.request.GET.get("scope", "all")
        return ctx

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "ticket_detail.html"
    context_object_name = "ticket"

    def get_queryset(self):
        qs = super().get_queryset().select_related("submitted_by")
        if not self.request.user.is_manager:
            qs = qs.filter(submitted_by=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_manager:
            ctx["status_form"] = StatusUpdateForm(instance=self.object)
        return ctx

class TicketCreateView(LoginRequiredMixin, CreateView):

    model = Ticket
    form_class = TicketForm
    template_name = "ticket_form.html"
    success_url = reverse_lazy("tickets:list")

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Ticket #{self.object.pk} raised.")
        return response

class TicketStatusUpdateView(ManagerRequiredMixin, View):
    """POST-only endpoint for updating a ticket's status."""

    http_method_names = ["post"]

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)
        form = StatusUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Status updated to {ticket.get_status_display()}.",
            )
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
        return redirect("tickets:detail", pk=pk)