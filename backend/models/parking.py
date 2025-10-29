# backend/models/parking.py

from backend.models.users import db
from datetime import datetime

class ParkingLot(db.Model):
    """Represents a parking lot with multiple spots."""
    __tablename__ = 'parking_lots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.Text, nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    
    spots = db.relationship('ParkingSpot', back_populates='lot', lazy='dynamic', cascade="all, delete-orphan")

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "pin_code": self.pin_code,
            "price_per_hour": self.price_per_hour,
            "capacity": self.capacity,
            "available_spots": self.spots.filter_by(status='Available').count()
        }

class ParkingSpot(db.Model):
    """Represents a single parking spot within a lot."""
    __tablename__ = 'parking_spots'

    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Available')
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lots.id'), nullable=False)
    
    lot = db.relationship('ParkingLot', back_populates='spots')
    bookings = db.relationship('Booking', back_populates='spot', lazy='dynamic', cascade="all, delete-orphan")

    def to_dict(self):
        """Serializes the object to a dictionary."""
        current_booking_info = {}
        occupant_username = None  # Initialize occupant username

        if self.status == 'Occupied':
            # Find the active booking for this spot
            booking = self.bookings.filter_by(park_out_time=None).first()
            if booking:
                current_booking_info = {
                    "booking_id": booking.id,
                    "user_id": booking.user_id,
                    "park_in_time": booking.park_in_time.isoformat()
                }
                # If a booking exists, get the user's username
                if booking.user:
                    occupant_username = booking.user.username

        return {
            "id": self.id,
            "spot_number": self.spot_number,
            "status": self.status, # The frontend should use this directly
            "lot_id": self.lot_id,
            # --- NEWLY ADDED FIELDS ---
            "lot_name": self.lot.name if self.lot else "N/A",
            "occupant_username": occupant_username,
            # This contains original details if needed
            "current_booking_info": current_booking_info
        }

class Booking(db.Model):
    """Represents a reservation of a parking spot by a user."""
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # --- FIX ---
    # The ondelete='RESTRICT' rule has been removed to allow manual deletion.
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spots.id'), nullable=False)
    
    park_in_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    park_out_time = db.Column(db.DateTime, nullable=True)
    cost = db.Column(db.Float, nullable=True)
    
    user = db.relationship('User', back_populates='bookings')
    spot = db.relationship('ParkingSpot', back_populates='bookings')

    def to_dict(self):
        """Serializes the Booking object to a dictionary."""
        # Check if spot and lot exist before accessing them
        lot_name = self.spot.lot.name if self.spot and self.spot.lot else "N/A"
        spot_number = self.spot.spot_number if self.spot else "N/A"
        # --- NEWLY ADDED FIELD ---
        lot_address = self.spot.lot.address if self.spot and self.spot.lot else "N/A"

        return {
            "id": self.id,
            "user_id": self.user_id,
            "spot_id": self.spot_id,
            "lot_name": lot_name,
            "spot_number": spot_number,
            "lot_address": lot_address, # For the active booking card
            # --- RENAMED KEYS TO MATCH FRONTEND ---
            "start_time": self.park_in_time.isoformat() if self.park_in_time else None,
            "end_time": self.park_out_time.isoformat() if self.park_out_time else None,
            "cost": self.cost
        }