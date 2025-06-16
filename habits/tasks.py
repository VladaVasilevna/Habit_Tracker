import logging

from celery import shared_task
from django.utils import timezone

from .management.telegram.telegram_sync import send_telegram_message_sync
from .models import Habit

logger = logging.getLogger(__name__)


@shared_task
def check_habits_and_send_reminders():
    """Проверяет привычки и отправляет напоминания"""
    now = timezone.localtime(timezone.now())
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour, time__minute=current_time.minute
    ).select_related("owner")

    logger.info(f"Found {habits.count()} habits to remind")

    for habit in habits:
        if habit.owner and habit.owner.telegram_chat_id:
            send_habit_reminder.delay(habit.id)
        else:
            logger.warning(f"Habit {habit.id} has no owner or telegram_chat_id")

    return f"Checked {habits.count()} habits"


@shared_task(bind=True)
def send_habit_reminder(self, habit_id):
    """Синхронная задача для отправки напоминания"""
    try:
        from habits.models import Habit

        habit = Habit.objects.select_related("owner").get(id=habit_id)

        if not habit.owner:
            return "Ошибка: Привычка не имеет владельца"

        if not habit.owner.telegram_chat_id:
            return "Ошибка: У владельца не указан Telegram Chat ID"

        message = (
            f"⏰ *Напоминание о привычке*\n"
            f"*Действие*: {habit.action}\n"
            f"*Место*: {habit.location}\n"
            f"*Время начала выполнения*: {habit.time.strftime('%H:%M')}\n"
            f"*Время выполнения*: {habit.execution_time}"
        )

        success, result = send_telegram_message_sync(
            chat_id=habit.owner.telegram_chat_id, text=message
        )

        if not success:
            raise ValueError(result)

        return result

    except Exception as e:
        logger.error(f"Ошибка в задаче send_habit_reminder: {str(e)}")
        raise self.retry(exc=e, countdown=60)
