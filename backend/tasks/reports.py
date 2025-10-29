# backend/tasks/reports.py

import os
import csv
from io import StringIO
from datetime import datetime, timedelta
from backend.celery_app import celery
from backend.models.users import User
from backend.models.parking import Booking

# Mock email function (replace with SMTP later)
def send_email(to_email, subject, body):
    print("--- SIMULATING EMAIL ---")
    print(f"To: {to_email}")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}")
    print("------------------------")

@celery.task(name="tasks.reports.send_monthly_reports")
def send_monthly_reports():
    """Generate and send monthly HTML reports to all users."""
    print("Starting monthly report generation...")
    users = User.query.filter_by(role='user').all()

    today = datetime.utcnow()
    first_day_current_month = today.replace(day=1)
    last_day_prev_month = first_day_current_month - timedelta(days=1)
    first_day_prev_month = last_day_prev_month.replace(day=1)

    for user in users:
        bookings = Booking.query.filter(
            Booking.user_id == user.id,
            Booking.leaving_timestamp.between(first_day_prev_month, last_day_prev_month)
        ).all()

        if not bookings:
            continue

        total_spent = sum(b.parking_cost or 0 for b in bookings)

        html_body = f"""
        <h1>Your Monthly Parking Summary</h1>
        <p>Hi {user.username},</p>
        <p>Here's your activity report for last month:</p>
        <ul>
            <li>Total Bookings: {len(bookings)}</li>
            <li>Total Spent: ₹{total_spent:.2f}</li>
        </ul>
        <p>Thanks for using our service!</p>
        """

        send_email(user.email, "Your Monthly Parking Report", html_body)

    print("Monthly reports sent.")
    return "Monthly reports generated successfully."

@celery.task(name="tasks.exports.export_parking_history_csv")
def export_parking_history_csv(user_id):
    """Generate CSV of user's entire parking history and send via email."""
    user = User.query.get(user_id)
    if not user:
        return "User not found."

    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.parking_timestamp.desc()).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Booking ID', 'Lot ID', 'Spot ID', 'Parked In', 'Parked Out', 'Cost'])

    for booking in bookings:
        writer.writerow([
            booking.id,
            booking.lot_id,
            booking.spot_id,
            booking.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S') if booking.parking_timestamp else 'N/A',
            booking.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if booking.leaving_timestamp else 'N/A',
            f"₹{booking.parking_cost:.2f}" if booking.parking_cost is not None else 'N/A'
        ])

    csv_data = output.getvalue()

    subject = "Your Parking History CSV Export"
    body = f"Hi {user.username},\n\nAttached is your parking history CSV:\n\n{csv_data}"
    send_email(user.email, subject, body)

    return f"CSV export for user {user.username} completed."
