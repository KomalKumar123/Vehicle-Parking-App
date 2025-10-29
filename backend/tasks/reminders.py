# backend/tasks/reminders.py

import os
from datetime import datetime, timedelta
from celery_app import celery
from backend.models.users import User
from backend.models.parking import Booking

# Configurable days from .env
REMINDER_INACTIVITY_DAYS = int(os.getenv("REMINDER_INACTIVITY_DAYS", "7"))

# Mock Google Chat notification
def send_gchat_notification(message):
    """Simulate sending a Google Chat notification."""
    print(f"--- SIMULATING GCHAT NOTIFICATION ---\n{message}\n---------------------------------")

@celery.task(name="tasks.reminders.send_daily_reminders")
def send_daily_reminders():
    """
    Sends a reminder to users who haven't booked in the last REMINDER_INACTIVITY_DAYS days.
    This task is scheduled to run daily via Celery Beat.
    """
    print("Checking for inactive users to send reminders...")
    cutoff_date = datetime.utcnow() - timedelta(days=REMINDER_INACTIVITY_DAYS)

    users = User.query.filter_by(role='user').all()

    for user in users:
        last_booking = (
            Booking.query.filter_by(user_id=user.id)
            .order_by(Booking.parking_timestamp.desc())
            .first()
        )

        if not last_booking or last_booking.parking_timestamp < cutoff_date:
            message = (
                f"Hi {user.username}! It's been a while. "
                f"Don't forget to book a parking spot if you need one!"
            )
            send_gchat_notification(message)

    return f"Daily reminders completed for inactivity > {REMINDER_INACTIVITY_DAYS} days."
