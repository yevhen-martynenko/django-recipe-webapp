import secrets
import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.users.models import ActivationCode


def send_email(user, subject, template, base_url):
    try:
        ActivationCode.objects.filter(user=user).delete()

        code = secrets.token_urlsafe(32)
        ActivationCode.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + datetime.timedelta(hours=24)
        )

        uid = urlsafe_base64_encode(force_bytes(user.id))
        code_encoded = urlsafe_base64_encode(force_bytes(code))

        link = f'{base_url}?uid={uid}&code={code_encoded}'

        message = render_to_string(
            template,
            {
                'user': user,
                'link': link,
            }
        )

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[user.email],
        )
        email.content_subtype = 'html'
        email.send()

        return True

    except Exception as e:
        raise e
        # message.error(f"Failed to send activation email to {user.email}: {str(e)}")
        # logger.error(f"Failed to send activation email to {user.email}: {str(e)}")


def send_activation_email(user):
    return send_email(
        user=user,
        subject='Activate your account',
        template='email/activate_account.html',
        base_url=settings.ACTIVATION_LINK_URL
    )


def send_password_reset_email(user):
    return send_email(
        user=user,
        subject='Reset Your Password',
        template='email/password_reset.html',
        base_url=f'{settings.PASSWORD_RESET_URL}confirm'
    )
