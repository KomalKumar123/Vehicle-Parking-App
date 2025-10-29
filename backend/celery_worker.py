# backend/celery_worker.py

from backend.app import create_app
from backend.celery_app import celery # Import the instance from our new file
from celery.schedules import crontab

# Create the Flask app to get its config
flask_app = create_app()

# Update the celery config with the app's config
# The namespace='CELERY' means all celery-related config keys should be uppercase and start with CELERY_
celery.config_from_object(flask_app.config, namespace='CELERY')

# Define the Celery beat schedule for periodic tasks
celery.conf.beat_schedule = {
    # Executes daily at 7 PM
    'send-daily-reminders': {
        'task': 'tasks.reminders.send_daily_reminders',
        'schedule': crontab(hour=19, minute=0),
    },
    # Executes on the first day of the month at midnight
    'send-monthly-reports': {
        'task': 'tasks.reports.send_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}

# Add the application context to the tasks
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
