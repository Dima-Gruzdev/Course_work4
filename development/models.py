from django.db import models

from config import settings


class MailingClient(models.Model):
    email = models.EmailField(
        unique=True, verbose_name="Email", help_text="Введите email клиента"
    )
    fio = models.CharField(
        max_length=255,
        verbose_name="Ф.И.О.",
        help_text="Фамилия, имя, отчество клиента.",
    )
    comment = models.TextField(
        verbose_name="Комментарий",
        blank=True,
        null=True,
        help_text="Дополнительная информация о клиенте.",
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["fio"]

    def __str__(self):
        return f"{self.fio} ({self.email})"
