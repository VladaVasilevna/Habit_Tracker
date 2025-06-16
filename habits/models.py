from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Habit(models.Model):
    location = models.CharField(
        max_length=255,
        verbose_name="Место",
        help_text="Место, в котором необходимо выполнять привычку.",
    )
    time = models.TimeField(
        verbose_name="Время", help_text="Время, когда необходимо выполнять привычку."
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Опишите действие, которое будет выполнять привычка.",
    )

    is_enjoyable = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Признак, является ли привычка приятной.",
    )
    related_habit = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        help_text="Связанная привычка, если она полезная.",
    )

    periodicity = models.PositiveIntegerField(
        default=1,
        verbose_name="Переодичность",
        help_text="Периодичность выполнения привычки в днях.",
    )
    reward = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Вознаграждение",
        help_text="Вознаграждение за выполнение привычки.",
    )
    execution_time = models.PositiveIntegerField(
        verbose_name="Время на выполнение",
        help_text="Время на выполнение привычки в секундах.",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Публичность",
        help_text="Признак публичности привычки.",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец привычки",
        help_text="Укажите владельца привычки",
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата создания привычки",
    )
    last_notification_sent = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата последнего уведомления",
        help_text="Когда в последний раз отправлялось уведомление",
    )

    def clean(self):
        if self.is_enjoyable and self.reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")

        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя указывать одновременно вознаграждение и связанную привычку."
            )

        if self.execution_time > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        if self.is_enjoyable and self.related_habit is not None:
            if not self.related_habit.is_enjoyable:
                raise ValidationError("Связанная привычка должна быть приятной.")

        if self.periodicity < 1:
            raise ValidationError("Периодичность должна быть не менее 1 дня.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызов валидаторов
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner.username}: {self.action} в {self.location} в {self.time}"


class HabitAchievement(models.Model):
    habit = models.ForeignKey(
        "Habit", on_delete=models.CASCADE, verbose_name="Привычка"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    date_completed = models.DateField(
        default=timezone.now,
        verbose_name="Дата выполнения",
        help_text="Дата выполнения привычки.",
    )
    status = models.BooleanField(
        default=False,
        verbose_name="Статус",
        help_text="Статус выполнения привычки: выполнена или нет.",
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Заметки",
        help_text="Заметки о выполнении привычки.",
    )

    def clean(self):
        if self.habit.user != self.user:
            raise ValidationError("Эта привычка не принадлежит пользователю.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.habit.action} выполнена: {'Да' if self.status else 'Нет'}"
