import os
from celery import Celery
from  django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reservation_service.settings')

app = Celery('reservation_service')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
