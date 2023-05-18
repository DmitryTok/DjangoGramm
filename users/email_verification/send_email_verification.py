from typing import Dict

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users import models


def gen_message(context_data: Dict) -> str:
    message = render_to_string(
        'registration/verify_email.html',
        context=context_data,
    )
    return message


def send_email_to_user(message_data: str, user_data) -> int:
    email = EmailMessage(
        'Verify email',
        message_data,
        to=[user_data.email],
    )
    return email.send()


def send_email_verification(request: HttpRequest, user: models.User) -> None:
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    gen_message(context)
    send_email_to_user(gen_message(context), user)
