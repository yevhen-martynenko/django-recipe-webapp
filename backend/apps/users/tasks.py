import secrets
import datetime

from django.conf import settings
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.users.models import ActivationCode


def send_activation_email(user):
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

        activation_link = f'{settings.ACTIVATION_LINK_URL}?uid={uid}&code={code_encoded}'

        subject = 'Activate your account'
        message = render_to_string(
            'email/activate_account.html',
            {
                'user': user,
                'activation_link': activation_link,
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
    except Exception as e:
        raise e
        # message.error(f"Failed to send activation email to {user.email}: {str(e)}")
        # logger.error(f"Failed to send activation email to {user.email}: {str(e)}")
