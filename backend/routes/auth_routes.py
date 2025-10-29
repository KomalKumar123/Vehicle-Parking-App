# backend/routes/auth_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
# **FIX:** Corrected the import to match the 'user.py' model file.
from backend.models.users import User, db

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint.
    Expects 'username', 'email', and 'password' in the JSON body.
    """
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # --- Input Validation ---
    if not all([username, email, password]):
        return jsonify({"msg": "Missing username, email, or password"}), 400
    
    is_valid_username, username_msg = User.validate_username(username)
    if not is_valid_username:
        return jsonify({"msg": username_msg}), 400
        
    # is_valid_email, email_msg = User.validate_email(email)
    # if not is_valid_email:
        # return jsonify({"msg": email_msg}), 400

    # --- Check for existing user ---
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already registered"}), 409

    # --- Create new user ---
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to create user. Please try again."}), 500

    return jsonify({"msg": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User and Admin login endpoint.
    Expects 'email' and 'password' in the JSON body.
    """
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400
        
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Use user.id as the identity and store the role in additional_claims.
        additional_claims = {"role": user.role}
        access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad email or password"}), 401
