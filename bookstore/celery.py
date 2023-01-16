
from __future__ import absolute_import
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

# здесь вы меняете имя
app = Celery("bookstore")

app.conf.broker_url = 'redis://shop_redis:6379/0'

app.conf.result_backend = 'redis://shop_redis:6379/0'

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()