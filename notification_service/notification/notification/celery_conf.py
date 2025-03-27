import os
from celery import Celery
from  django.conf import settings
from kombu import Exchange, Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notification.settings')

app = Celery('notification', broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_queues = (
    Queue('reservation_notifications_queue', Exchange('reservation_notifications'), routing_key='reservation.notify', exchange_type='direct'),
)

app.conf.task_routes = {
    'email_notification.tasks.process_notification': {'queue': 'reservation_notifications_queue', 'routing_key': 'reservation.notify'},
}

app.autodiscover_tasks(['email_notification'])



# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
