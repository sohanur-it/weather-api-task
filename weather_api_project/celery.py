from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_api_project.settings')
app = Celery('weather_api_project')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # Executes at sunset in Melbourne
    'start-periodic-tasks-1': {
        'task': 'BDWeather.tasks.fetch_district',
        'schedule': crontab(minute='*/60'),
        # 'args': (16, 16),
    },
    'start-periodic-tasks-2': {
        'task': 'BDWeather.tasks.fetch_temp_each_dist',
        'schedule': crontab(minute='*/60'),
        # 'args': (16, 16),
    },
}