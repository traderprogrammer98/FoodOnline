from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_verification_email(request, user, mail_subject, email_template, view_name="verify_email"):
    subject = mail_subject
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    message = render_to_string(email_template, {
        'user': user,
        'verification_link': request.build_absolute_uri(
            reverse(view_name, kwargs={'uidb64': uid, 'token': token})
        )
    })
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype = "html"
    email.send()
