from django.shortcuts import render
from mailings.models import Mailing
from development.models import MailingClient


def home(request):
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="running").count()
    unique_clients = MailingClient.objects.count()

    context = {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_clients": unique_clients,
    }
    return render(request, "home.html", context)
