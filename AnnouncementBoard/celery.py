import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AnnouncementBoard.settings')

app = Celery('AnnouncementBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_mail': {
        'task': 'board.tasks.send_weekly_mail',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
