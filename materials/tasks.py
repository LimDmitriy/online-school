from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from materials.models import Subscription


@shared_task
def send_course_update_email(course_id):
    subscriptions = Subscription.objects.filter(course_id=course_id)

    emails = [
        subscription.user.email
        for subscription in subscriptions
        if subscription.user.email
    ]
    if not emails:
        return

    send_mail(
        subject="Обновление курса",
        message="Ваш курс был обновлен",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=emails,
        fail_silently=False,
    )
