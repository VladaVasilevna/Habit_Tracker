import asyncio

from django.core.management.base import BaseCommand

from habits.management.telegram.habit_bot import setup_bot


class Command(BaseCommand):
    """Запуск Telegram бота."""

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Telegram bot..."))

        application = setup_bot()

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(application.run_polling())
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS("Stopping bot..."))
        finally:
            loop.close()
