from django import forms

from .models import Ticket


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ["name", "area", "severity", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 5:
            raise forms.ValidationError("Please include your full name and surname")
        return name

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if len(description) < 20:
            raise forms.ValidationError(
                "Description must be at least 20 characters"
            )
        return description


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["status"]

    def clean_status(self):
        status = self.cleaned_data["status"]
        valid = {value for value, _ in Ticket.Status.choices}
        if status not in valid:
            raise forms.ValidationError("Invalid status.")
        return status
