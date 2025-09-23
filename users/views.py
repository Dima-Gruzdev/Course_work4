from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from .forms import UserRegisterForm, CustomLoginForm, ProfileForm


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        messages.success(
            self.request,
            f"Регистрация успешна! Приветственное письмо отправлено на {user.email}.",
        )
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = "Добро пожаловать!"
        message = "Здравствуйте! Спасибо за регистрацию на нашем сайте."
        from_email = "nubile4446@mail.ru"
        recipient_list = [user_email]
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            messages.error(self.request, f"Не удалось отправить письмо: {e}")


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "users/login.html"


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'users/profile.html', {'user': user})


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = '/users/profile/'  # или reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
