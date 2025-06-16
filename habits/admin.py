from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Habit


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        is_enjoyable = cleaned_data.get("is_enjoyable")
        reward = cleaned_data.get("reward")
        related_habit = cleaned_data.get("related_habit")
        execution_time = cleaned_data.get("execution_time")
        periodicity = cleaned_data.get("periodicity")

        if is_enjoyable and reward:
            raise ValidationError("У приятной привычки не может быть вознаграждения.")

        if reward and related_habit:
            raise ValidationError(
                "Нельзя указывать одновременно вознаграждение и связанную привычку."
            )

        if execution_time and execution_time > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд.")

        if is_enjoyable and related_habit and not related_habit.is_enjoyable:
            raise ValidationError("Связанная привычка должна быть приятной.")

        if periodicity and periodicity < 1:
            raise ValidationError("Периодичность должна быть не менее 1 дня.")

        return cleaned_data


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    form = HabitForm
    list_display = (
        "action",
        "owner_info",
        "time_display",
        "location",
        "is_enjoyable",
        "periodicity_display",
        "execution_time_display",
        "is_public",
    )
    list_filter = ("is_enjoyable", "is_public", "owner")
    search_fields = ("action", "location", "owner__username")
    readonly_fields = ("created_date", "last_notification_sent")

    def owner_info(self, obj):
        return obj.owner.username if obj.owner else "-"

    owner_info.short_description = "Владелец"

    def time_display(self, obj):
        return obj.time.strftime("%H:%M") if obj.time else "-"

    time_display.short_description = "Время"

    def periodicity_display(self, obj):
        return f"{obj.periodicity} дней" if obj.periodicity else "-"

    periodicity_display.short_description = "Периодичность"

    def execution_time_display(self, obj):
        return f"{obj.execution_time} сек" if obj.execution_time else "-"

    execution_time_display.short_description = "Время выполнения"
