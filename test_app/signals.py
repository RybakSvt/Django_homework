"""
Сигналы для уведомлений об изменении статуса задач.

Логика:
1. Отслеживает изменения поля 'status' модели Task
2. При изменении отправляет email владельцу задачи
3. Имеет защиту от спама: не отправляет при частых изменениях (30 сек)
4. Для статуса 'done' отправляет специальное уведомление о закрытии

Настройки:
- EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
- Письма выводятся в консоль Django
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.cache import cache
from .models import Task
import logging

logger = logging.getLogger(__name__)

_previous_status_cache = {}


@receiver(pre_save, sender=Task)
def save_previous_status(sender, instance, **kwargs):
    """Сохраняет старый статус задачи перед сохранением."""
    try:
        if instance.pk:
            old_task = Task.objects.get(pk=instance.pk)
            _previous_status_cache[instance.pk] = old_task.status
            logger.debug(f"Saved previous status for task {instance.pk}: {old_task.status}")
        else:
            _previous_status_cache[instance.pk] = None
    except Task.DoesNotExist:
        _previous_status_cache[instance.pk] = None


@receiver(post_save, sender=Task)
def notify_on_status_change(sender, instance, created, **kwargs):
    """Отправляет email при изменении статуса задачи."""

    if created:
        return

    old_status = _previous_status_cache.get(instance.pk)
    new_status = instance.status

    if old_status == new_status:
        return

    cache_key = f"task_notification_cooldown_{instance.pk}"

    if cache.get(cache_key):
        logger.info(f"Skipping notification for task {instance.pk} (cooldown active)")
        print(f"Notification skipped for task {instance.pk} - too frequent changes")
        return

    cache.set(cache_key, True, timeout=30)

    if instance.pk in _previous_status_cache:
        del _previous_status_cache[instance.pk]

    if not instance.owner or not instance.owner.email:
        logger.warning(f"Cannot send notification: task {instance.pk} has no owner or email")
        return

    send_status_change_email(instance, old_status, new_status)


def send_status_change_email(task, old_status, new_status):
    """Формирует и отправляет email о изменении статуса."""

    is_closing = (new_status == 'done')

    subject = "Статус задачи изменён" if not is_closing else "Задача закрыта!"

    context = {
        'task_title': task.title,
        'old_status': old_status,
        'new_status': new_status,
        'owner_name': task.owner.username,
        'task_url': f"http://localhost:8000/api/tasks/{task.id}/",
        'is_closing': is_closing,
    }

    message = f"""
    Здравствуйте, {task.owner.username}!

    Статус вашей задачи "{task.title}" был изменён.

    Старый статус: {old_status}
    Новый статус: {new_status}

    {"Задача закрыта!" if is_closing else "Продолжайте работу!"}

    Ссылка на задачу: http://localhost:8000/api/v1/tasks/{task.id}/
    """

    html_message = render_to_string('emails/task_status_change.html', context)

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@taskmanager.com',
            recipient_list=[task.owner.email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Email sent to {task.owner.email} for task {task.pk}")
        print(f"Email sent to {task.owner.email} | Task: {task.title} | Status: {old_status} -> {new_status}")

    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        print(f"Email error: {e}")