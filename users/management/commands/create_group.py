from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Mailing, MailingAttempt
from development.models import MailingClient


class Command(BaseCommand):
    help = 'Создаёт группу "Менеджер" с правами на просмотр'

    def handle(self, *args, **options):
        manager_group, created = Group.objects.get_or_create(name='Менеджер')
        if created:
            self.stdout.write(
                self.style.SUCCESS('Группа "Менеджер" успешно создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Менеджер" уже существует')
            )

        mailing_ct = ContentType.objects.get_for_model(Mailing)
        attempt_ct = ContentType.objects.get_for_model(MailingAttempt)
        client_ct = ContentType.objects.get_for_model(MailingClient)

        view_mailing = Permission.objects.get(content_type=mailing_ct, codename='view_mailing')
        view_attempt = Permission.objects.get(content_type=attempt_ct, codename='view_mailingattempt')
        view_client = Permission.objects.get(content_type=client_ct, codename='view_client')

        manager_group.permissions.add(view_mailing, view_attempt, view_client)

        self.stdout.write(
            self.style.SUCCESS('Права для группы "Менеджер" установлены')
        )
