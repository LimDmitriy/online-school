import time
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from materials.models import Subscription


@shared_task
def send_course_update_email(course_id):
    """Отправляет сообщения при обновлении курсов или уроков"""
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


User = get_user_model()


@shared_task
def deactivate_users():
    """Блокирует пользователей не заходивших более 30 дней"""
    month_ago = timezone.now() - timedelta(days=30)

    User.objects.filter(
        last_login__lt=month_ago,
        is_active=True,
    ).update(is_active=False)
