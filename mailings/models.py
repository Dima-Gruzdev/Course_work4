from django.db import models

from config import settings
from development.models import MailingClient


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject


STATUS_CHOICES = (
    ("created", "Создана"),
    ("running", "Запущена"),
    ("completed", "Завершена"),
)


class Mailing(models.Model):
    start_date = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_date = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="created",
        verbose_name="Статус рассылки",
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    clients = models.ManyToManyField(MailingClient, verbose_name="Получатели")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"Рассылка {self.start_date} — {self.message.subject}"


ATTEMPT_STATUS_CHOICES = (
    ("success", "Успешно"),
    ("failed", "Не успешно"),
)


class MailingAttempt(models.Model):
    attempt_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время попытки"
    )
    status = models.CharField(
        max_length=10, choices=ATTEMPT_STATUS_CHOICES, verbose_name="Статус"
    )
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ почтового сервера"
    )
    mailing = models.ForeignKey(
        "mailings.Mailing", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылок"

    def __str__(self):
        return f"{self.mailing} — {self.get_status_display()} ({self.attempt_date})"
