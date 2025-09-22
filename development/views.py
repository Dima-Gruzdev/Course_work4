from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import MailingClient
from .forms import ClientForm


@method_decorator(cache_page(60 * 15), name="dispatch")
class ClientListView(ListView):
    """Список всех клиентов"""

    model = MailingClient
    template_name = "clients/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return MailingClient.objects.filter(owner=self.request.user)


@method_decorator(cache_page(60 * 15), name="dispatch")
class ClientDetailView(DetailView):
    """Просмотр одного клиента"""

    model = MailingClient
    template_name = "clients/client_detail.html"
    context_object_name = "client"

    def get_queryset(self):
        return MailingClient.objects.filter(owner=self.request.user)


class ClientCreateView(CreateView):
    """Создание клиента"""

    model = MailingClient
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("development:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user  # Привязываем к текущему пользователю
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    """Редактирование клиента"""

    model = MailingClient
    form_class = ClientForm
    template_name = "clients/client_form.html"
    success_url = reverse_lazy("development:client_list")

    def get_queryset(self):
        return MailingClient.objects.filter(owner=self.request.user)


class ClientDeleteView(DeleteView):
    """Удаление клиента"""

    model = MailingClient
    template_name = "clients/client_confirm_delete.html"
    success_url = reverse_lazy("development:client_list")
