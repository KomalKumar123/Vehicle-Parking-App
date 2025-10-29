# backend/routes/user_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from datetime import datetime
import math

from backend.models.users import db, User
from backend.models.parking import ParkingLot, ParkingSpot, Booking
from backend.tasks.reports import export_parking_history_csv  # Adjust path if moved to tasks/exports.py
from backend.celery_app import celery
from celery.result import AsyncResult

user_bp = Blueprint('user_bp', __name__)

# --- User Dashboard and Booking ---

@user_bp.route('/lots', methods=['GET'])
@jwt_required()
def get_available_lots():
    """User: View all parking lots and their availability."""
    lots = ParkingLot.query.all()
    return jsonify([lot.to_dict() for lot in lots]), 200


@user_bp.route('/book/<int:lot_id>', methods=['POST'])
@jwt_required()
def book_spot(lot_id):
    """User: Book the first available spot in a chosen lot."""
    user_id = get_jwt_identity()

    # Check if the user already has an active booking
    active_booking = Booking.query.filter_by(user_id=user_id, park_out_time=None).first()
    if active_booking:
        return jsonify(msg="You already have an active booking."), 409

    # Find the first available spot in the specified lot
    parking_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='Available').first()
    if not parking_spot:
        return jsonify(msg="Sorry, no available spots in this parking lot."), 404

    # Change spot status and create a new booking record
    parking_spot.status = 'Occupied'
    new_booking = Booking(user_id=user_id, spot_id=parking_spot.id)
    db.session.add(new_booking)
    db.session.commit()

    return jsonify(
        msg="Spot booked successfully!", 
        booking_details=new_booking.to_dict()
    ), 201


@user_bp.route('/booking/active', methods=['GET'])
@jwt_required()
def get_active_booking():
    """User: View their current active booking details."""
    user_id = get_jwt_identity()
    active_booking = Booking.query.filter_by(user_id=user_id, park_out_time=None).first()

    if not active_booking:
        return jsonify(msg="No active booking found."), 404
        
    return jsonify(active_booking.to_dict()), 200


@user_bp.route('/booking/release', methods=['POST'])
@jwt_required()
def release_spot():
    """User: Release their spot, calculate cost, and end the booking."""
    user_id = get_jwt_identity()
    
    # Find the active booking for the user
    booking = Booking.query.filter_by(user_id=user_id, park_out_time=None).first()
    if not booking:
        return jsonify(msg="No active booking to release."), 404

    # Update booking details
    booking.park_out_time = datetime.utcnow()
    
    # Calculate cost
    duration_seconds = (booking.park_out_time - booking.park_in_time).total_seconds()
    duration_hours = math.ceil(duration_seconds / 3600)  # Round up to the next hour
    price_per_hour = booking.spot.lot.price_per_hour
    booking.cost = duration_hours * price_per_hour

    # Update the spot status back to 'Available'
    booking.spot.status = 'Available'
    
    db.session.commit()

    return jsonify(
        msg="Parking spot released successfully.",
        receipt=booking.to_dict()
    ), 200


# --- User Dashboard Data ---

@user_bp.route('/dashboard/summary', methods=['GET'])
@jwt_required()
def get_user_dashboard_summary():
    """User: Get summary data for their personal dashboard."""
    user_id = get_jwt_identity()
    
    # Total bookings and total spent
    user_stats = db.session.query(
        func.count(Booking.id).label('total_bookings'),
        func.sum(Booking.cost).label('total_spent')
    ).filter(Booking.user_id == user_id).first()

    # Most recent booking
    recent_booking = Booking.query.filter_by(user_id=user_id).order_by(Booking.park_in_time.desc()).first()

    return jsonify({
        "total_bookings": user_stats.total_bookings or 0,
        "total_spent": user_stats.total_spent or 0.0,
        "recent_booking": recent_booking.to_dict() if recent_booking else None
    }), 200


@user_bp.route('/history', methods=['GET'])
@jwt_required()
def get_booking_history():
    """User: Get their own completed booking history."""
    user_id = get_jwt_identity()
    
    history = Booking.query.filter(
        Booking.user_id == user_id,
        Booking.park_out_time.isnot(None)
    ).order_by(Booking.park_out_time.desc()).all()
    
    return jsonify([b.to_dict() for b in history]), 200


# --- CSV Export Trigger and Task Status ---

@user_bp.route('/export/csv', methods=['POST'])
@jwt_required()
def trigger_csv_export():
    """User: Trigger an asynchronous CSV export of their parking history."""
    user_id = get_jwt_identity()
    task = export_parking_history_csv.delay(user_id)
    return jsonify(
        msg="Your parking history export has started. You will receive an email when it's ready.",
        task_id=task.id
    ), 202


@user_bp.route('/task/status/<task_id>', methods=['GET'])
@jwt_required()
def get_task_status(task_id):
    """Check the status of a Celery background task."""
    result = AsyncResult(task_id, app=celery)
    return jsonify({
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None
    }), 200
