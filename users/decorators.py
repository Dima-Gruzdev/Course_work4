from functools import wraps
from django.shortcuts import redirect, get_object_or_404

from development.models import MailingClient


def user_owns_client(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        client = get_object_or_404(MailingClient, pk=kwargs["pk"])
        if client.owner != request.user and not request.user.is_manager:
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper
