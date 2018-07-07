from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerybeat.settings')

app = Celery('celerybeat',
             broker='redis://localhost:6379',
             backend='django-db',
             include=['celerybeat.tasks'],)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
#app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
#app.autodiscover_tasks()


app.conf.update(
    result_expires=3600,
)


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


if __name__ == '__main__':
    app.start()