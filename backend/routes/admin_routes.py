# backend/routes/admin_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
from backend.models.users import db, User
from backend.models.parking import ParkingLot, ParkingSpot, Booking
from sqlalchemy import func, case
from sqlalchemy.exc import IntegrityError

admin_bp = Blueprint('admin_bp', __name__)

# --- Custom Decorator for Admin Access ---
def admin_required():
    """A decorator to protect routes that should only be accessible by admins."""
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return jsonify(msg="Admins only! Access forbidden."), 403
            else:
                return fn(*args, **kwargs)
        return decorator
    return wrapper


# --- Parking Lot Management ---

@admin_bp.route('/lots', methods=['POST'])
@admin_required()
def create_parking_lot():
    """Admin: Create a new parking lot."""
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    pin_code = data.get('pin_code')
    price = data.get('price_per_hour')
    capacity = data.get('capacity')

    if not all([name, address, pin_code, price, capacity]):
        return jsonify(msg="Missing required fields"), 400
    
    if not isinstance(capacity, int) or capacity <= 0:
        return jsonify(msg="Capacity must be a positive integer"), 400

    if ParkingLot.query.filter_by(name=name).first():
        return jsonify(msg="A parking lot with this name already exists"), 409

    new_lot = ParkingLot(
        name=name, 
        address=address, 
        pin_code=pin_code,
        price_per_hour=price,
        capacity=capacity
    )
    db.session.add(new_lot)
    db.session.flush()

    for i in range(1, capacity + 1):
        spot = ParkingSpot(spot_number=i, lot_id=new_lot.id)
        db.session.add(spot)
    
    db.session.commit()
    return jsonify(msg="Parking lot and spots created successfully", lot=new_lot.to_dict()), 201


@admin_bp.route('/lots/<int:lot_id>', methods=['PUT'])
@admin_required()
def edit_parking_lot(lot_id):
    """Admin: Edit an existing parking lot."""
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()

    lot.name = data.get('name', lot.name)
    lot.address = data.get('address', lot.address)
    lot.pin_code = data.get('pin_code', lot.pin_code)
    lot.price_per_hour = data.get('price_per_hour', lot.price_per_hour)
    
    new_capacity = data.get('capacity')

    if new_capacity is not None and new_capacity != lot.capacity:
        if not isinstance(new_capacity, int) or new_capacity <= 0:
            return jsonify(msg="Capacity must be a positive integer"), 400
        
        current_spots_count = lot.spots.count()
        
        if new_capacity > current_spots_count:
            for i in range(current_spots_count + 1, new_capacity + 1):
                spot = ParkingSpot(spot_number=i, lot_id=lot.id)
                db.session.add(spot)
        elif new_capacity < current_spots_count:
            spots_to_remove_count = current_spots_count - new_capacity
            available_spots_to_remove = lot.spots.filter_by(status='Available').order_by(ParkingSpot.spot_number.desc()).limit(spots_to_remove_count).all()

            if len(available_spots_to_remove) < spots_to_remove_count:
                return jsonify(msg="Cannot reduce capacity. Not enough available spots to remove."), 409
            
            for spot in available_spots_to_remove:
                db.session.delete(spot)
        
        lot.capacity = new_capacity

    try:
        db.session.commit()
        
    except IntegrityError:
        db.session.rollback()
        return jsonify(msg="Update failed. Cannot remove a parking spot that has a booking history."), 409
        
    return jsonify(msg="Parking lot updated successfully", lot=lot.to_dict()), 200


@admin_bp.route('/lots', methods=['GET'])
@admin_required()
def get_all_parking_lots():
    """Admin: View all parking lots."""
    lots = ParkingLot.query.all()
    return jsonify([lot.to_dict() for lot in lots]), 200

@admin_bp.route('/lots/<int:lot_id>', methods=['DELETE'])
@admin_required()
def delete_parking_lot(lot_id):
    """Admin: Delete a parking lot and all its associated data if empty."""
    lot = ParkingLot.query.get_or_404(lot_id)

    # First, check if any spots are currently occupied.
    occupied_spots = lot.spots.filter_by(status='Occupied').count()
    if occupied_spots > 0:
        return jsonify(msg=f"Cannot delete lot. {occupied_spots} spot(s) are currently occupied."), 409
    
    try:
        spot_ids = [spot.id for spot in lot.spots]
        if spot_ids:
            # This is a bulk delete operation for efficiency.
            Booking.query.filter(Booking.spot_id.in_(spot_ids)).delete(synchronize_session=False)

        db.session.delete(lot)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

        print(f"An error occurred during deletion: {e}")
        return jsonify(msg="An unexpected error occurred during deletion. Please try again."), 500
        
    return jsonify(msg=f"Parking lot '{lot.name}' and all its history have been permanently deleted."), 200


# --- User and Spot Monitoring ---

@admin_bp.route('/users', methods=['GET'])
@admin_required()
def get_all_users():
    """Admin: View all registered users."""
    users = User.query.filter_by(role='user').all()
    return jsonify([user.to_dict() for user in users]), 200

@admin_bp.route('/spots/status', methods=['GET'])
@admin_required()
def get_all_spot_statuses():
    """Admin: View the status of all parking spots."""
    spots = ParkingSpot.query.order_by(ParkingSpot.lot_id, ParkingSpot.spot_number).all()
    return jsonify([spot.to_dict() for spot in spots]), 200


# --- Dashboard Data ---

@admin_bp.route('/dashboard/summary', methods=['GET'])
@admin_required()
def get_admin_dashboard_summary():
    """Admin: Get summary data for the dashboard."""
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    occupied_spots = ParkingSpot.query.filter_by(status='Occupied').count()
    available_spots = total_spots - occupied_spots
    
    lot_occupancy = db.session.query(
        ParkingLot.name,
        func.count(ParkingSpot.id).label('total'),
        func.sum(case((ParkingSpot.status == 'Occupied', 1), else_=0)).label('occupied')
    ).join(ParkingSpot).group_by(ParkingLot.name).all()

    lot_occupancy_data = [
        {
            "lot_name": name,
            "total_spots": total,
            "occupied_spots": occupied or 0,
            "available_spots": total - (occupied or 0)
        } for name, total, occupied in lot_occupancy
    ]

    return jsonify({
        "total_lots": total_lots,
        "total_spots": total_spots,
        "occupied_spots": occupied_spots,
        "available_spots": available_spots,
        "lot_occupancy": lot_occupancy_data
    }), 200

@admin_bp.route('/bookings', methods=['GET'])
@admin_required()
def get_all_bookings():
    """Admin: Get all booking history, with an optional filter by user_id."""
    query = Booking.query
    
    # Check if a user_id is provided in the query string (e.g., /bookings?user_id=2)
    user_id = request.args.get('user_id')
    if user_id:
        query = query.filter_by(user_id=user_id)
        
    all_bookings = query.order_by(Booking.park_in_time.desc()).all()
    
    return jsonify([b.to_dict() for b in all_bookings]), 200
