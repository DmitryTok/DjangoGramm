from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def gen_message(get_context):
    message = render_to_string(
        'registration/verify_email.html',
        context=get_context,
    )
    return message


def send_email_to_user(get_message, get_user):
    email = EmailMessage(
        'Verify email',
        get_message,
        to=[get_user.email],
    )
    return email.send()


def send_email_for_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token_generator.make_token(user),
    }
    gen_message(context)
    send_email_to_user(gen_message(context), user)
