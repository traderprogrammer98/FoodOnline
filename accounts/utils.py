from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_verification_email(request, user):
    subject = "Please verify your email"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    message = render_to_string("accounts/emails/account_verification_email.html", {
        'user': user,
        'verification_link': request.build_absolute_uri(
            reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
        )
    })
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype = "html"
    email.send()
