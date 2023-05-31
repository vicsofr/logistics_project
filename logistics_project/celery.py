import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')

app = Celery('logistics_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
