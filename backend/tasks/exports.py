import csv
import io
from celery import shared_task
from backend.models.parking import Booking
from datetime import datetime

@shared_task
def export_parking_history_csv(user_id):
    print(f"[EXPORT] Starting CSV export for user {user_id}")

    bookings = Booking.query.filter_by(user_id=user_id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Booking ID", "Parking Lot", "Spot Number", "Park In Time", "Park Out Time"])

    if bookings:
        for b in bookings:
            writer.writerow([
                b.id,
                b.parking_spot.parking_lot.name if b.parking_spot and b.parking_spot.parking_lot else "",
                b.parking_spot.spot_number if b.parking_spot else "",
                b.park_in_time.strftime("%Y-%m-%d %H:%M") if b.park_in_time else "",
                b.park_out_time.strftime("%Y-%m-%d %H:%M") if b.park_out_time else ""
            ])
    else:
        print(f"[EXPORT] No bookings found for user {user_id}")

    filename = f"parking_history_{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    csv_data = output.getvalue()
    mime_type = "text/csv"

    print(f"[EXPORT] Returning CSV with {len(bookings)} records for user {user_id}")
    return filename, csv_data, mime_type
