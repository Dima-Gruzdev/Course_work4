from django.shortcuts import get_object_or_404, redirect, render
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
from .models import Message, Mailing
from .forms import MessageForm, MailingForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageListView(ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"


@method_decorator(cache_page(60 * 15), name="dispatch")
class MessageDetailView(DetailView):
    model = Message
    template_name = "mailings/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailings/message_form.html"
    success_url = reverse_lazy("mailings:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("mailings:message_list")


@method_decorator(cache_page(60 * 15), name="dispatch")
class MailingListView(ListView):
    model = Mailing
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        return (
            Mailing.objects.all().select_related("message").prefetch_related("clients")
        )


class MailingDetailView(DetailView):
    model = Mailing
    template_name = "mailings/mailing_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["attempts"] = MailingAttempt.objects.filter(
            mailing=self.object
        ).order_by("-attempt_date")
        return context


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailings/mailing_form.html"
    success_url = reverse_lazy("mailings:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailings:mailing_list")


def send_mailing_now(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    try:
        recipients = [client.email for client in mailing.clients.all()]
        if not recipients:
            messages.error(request, "Нет получателей для этой рассылки.")
            return redirect("mailings:mailing_detail", pk=mailing.pk)

        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )
        MailingAttempt.objects.create(
            mailing=mailing,
            status="success",
            server_response="Письмо отправлено успешно.",
        )

        if mailing.status == "created":
            mailing.status = "running"
            mailing.save()

        messages.success(request, "Рассылка успешно отправлена!")

    except Exception as e:
        MailingAttempt.objects.create(
            mailing=mailing, status="failed", server_response=str(e)
        )
        messages.error(request, f"Ошибка при отправке: {e}")

    return redirect("mailing_detail", pk=mailing.pk)


from mailings.models import MailingAttempt


def stats(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    attempts = MailingAttempt.objects.filter(mailing__owner=request.user)

    total_attempts = attempts.count()
    success_count = attempts.filter(status="success").count()
    failed_count = attempts.filter(status="failed").count()

    context = {
        "total_attempts": total_attempts,
        "success_count": success_count,
        "failed_count": failed_count,
    }
    return render(request, "stats.html", context)
