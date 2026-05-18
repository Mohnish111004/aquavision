"""
Authentication routes: signup, login, profile
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db
from database.models import User
from utils.auth import create_access_token, token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    """Register a new user"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # Validate required fields
    required = ['username', 'email', 'password']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': 'Missing required fields', 'missing': missing}), 422
    
    username = data['username'].strip()
    email = data['email'].strip().lower()
    password = data['password']
    full_name = data.get('full_name', '').strip()
    
    # Validation
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 422
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 422
    
    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 422
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create new user
    user = User(
        username=username,
        email=email,
        full_name=full_name,
        role='user'
    )
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = create_access_token(user.id, user.username, user.role)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 422
    
    # Find user by username or email
    user = User.query.filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Generate token
    token = create_access_token(user.id, user.username, user.role)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/auth/profile', methods=['GET'])
@token_required
def get_profile():
    """Get current user profile"""
    user_id = request.current_user['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user.to_dict()}), 200


@auth_bp.route('/auth/profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    user_id = request.current_user['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # Update allowed fields
    if 'full_name' in data:
        user.full_name = data['full_name'].strip()
    
    if 'email' in data:
        new_email = data['email'].strip().lower()
        if new_email != user.email:
            # Check if email is already taken
            if User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'Email already in use'}), 409
            user.email = new_email
    
    if 'password' in data:
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 422
        user.set_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500
