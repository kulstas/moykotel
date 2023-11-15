import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moykotel.settings')

app = Celery('moykotel')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_newsletter_every_mon_at_8': {
        'task': 'newsletters.tasks.weekly_newsletter',
        'schedule': crontab(day_of_week='monday', hour='8'),
    },
}