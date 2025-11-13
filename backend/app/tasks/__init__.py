from app.tasks.celery_app import celery_app
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'cleanup-old-results': {
        'task': 'cleanup_old_results',
        'schedule': crontab(hour=3, minute=0),
    },
}
