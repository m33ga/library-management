from __future__ import absolute_import, unicode_literals

# Import Celery app as part of Django's default app setup
from .celery_conf import app as celery_app

__all__ = ('celery_app',)
