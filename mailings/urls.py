from django.urls import path
from . import views
from .apps import MailingsConfig

app_name = MailingsConfig.name

urlpatterns = [
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path(
        "messages/<int:pk>/", views.MessageDetailView.as_view(), name="message_detail"
    ),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("", views.MailingListView.as_view(), name="mailing_list"),
    path("<int:pk>/", views.MailingDetailView.as_view(), name="mailing_detail"),
    path("create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path("<int:pk>/update/", views.MailingUpdateView.as_view(), name="mailing_update"),
    path("<int:pk>/delete/", views.MailingDeleteView.as_view(), name="mailing_delete"),
    path("<int:pk>/send/", views.send_mailing_now, name="send_mailing_now"),
    path("stats/", views.stats, name="stats"),
]
