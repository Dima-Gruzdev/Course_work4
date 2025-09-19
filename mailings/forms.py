from django import forms
from .models import Message, Mailing
from development.models import MailingClient


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }


class MailingForm(forms.ModelForm):
    clients = forms.ModelMultipleChoiceField(
        queryset=MailingClient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Получатели",
    )

    class Meta:
        model = Mailing
        fields = ["start_date", "end_date", "message", "clients"]
        widgets = {
            "start_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "end_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "message": forms.Select(attrs={"class": "form-control"}),
        }
