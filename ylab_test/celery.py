import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ylab_test.settings')

app = Celery('ylab_test')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
