from celery import Celery
import os

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'root.settings'
)

app = Celery('root')

app.config_from_object(
    'django.conf:settings',
    namespace='CELERY'
)

app.autodiscover_tasks()