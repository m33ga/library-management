import json
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = 'Configure Celery Beat periodic tasks'

    def handle(self, *args, **kwargs):

        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )


        task_name = 'Check expired reservations'
        task, created = PeriodicTask.objects.get_or_create(
            name=task_name,
            defaults={
                'interval': schedule,
                'task': 'book_reservations.tasks.check_expired_reservations',
                'args': json.dumps([]),
            },
        )

        if not created:
            task.interval = schedule
            task.task = 'book_reservations.tasks.check_expired_reservations'
            task.args = json.dumps([])
            task.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'{"Created" if created else "Updated"} periodic task: {task_name}'
            )
        )
