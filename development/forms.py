from django import forms
from .models import MailingClient


class ClientForm(forms.ModelForm):
    class Meta:
        model = MailingClient
        fields = ["email", "fio", "comment"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "fio": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "email": "Email",
            "fio": "Ф.И.О.",
            "comment": "Комментарий",
        }
