from django.core.management.base import BaseCommand
from mailings.views import send_mailing_now
from django.http import HttpRequest


class Command(BaseCommand):
    help = "Отправить рассылку по ID"

    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int)

    def handle(self, *args, **options):
        request = HttpRequest()
        request.method = "POST"
        response = send_mailing_now(request, options["mailing_id"])
        self.stdout.write("Рассылка обработана.")
