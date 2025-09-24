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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # ← извлекаем user
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['message'].queryset = self.fields['message'].queryset.filter(owner=self.user)
            self.fields['clients'].queryset = MailingClient.objects.filter(owner=self.user)

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:
            instance.owner = self.user
        return super().save(commit)
