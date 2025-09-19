from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите название почты"}
        )

        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Придумайте пароль"}
        )

        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите повторно пароль"}
        )

        self.fields["city"].widget.attrs.update({"class": "form-control"})

        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Укажите номер телефона (необязательно)",
            }
        )

        self.fields["avatar"].widget.attrs.update({"class": "form-control"})

    class Meta:
        model = User
        fields = ("email", "password1", "password2", "city", "avatar", "phone_number")

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError(
                "Номер телефона должен состоять только из цифр."
            )
        return phone_number


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
            }
        )
