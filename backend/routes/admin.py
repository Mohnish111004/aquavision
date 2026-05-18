"""
Admin panel routes: user management, system statistics
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import func, desc
from database import db
from database.models import User, Prediction, SystemMetrics
from utils.auth import admin_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users (admin only)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '').strip()
    
    query = User.query
    
    # Search filter
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%')) |
            (User.full_name.ilike(f'%{search}%'))
        )
    
    # Pagination
    pagination = query.order_by(desc(User.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'users': [user.to_dict() for user in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    }), 200


@admin_bp.route('/admin/users/<int:user_id>', methods=['GET'])
@admin_required
def get_user_detail(user_id):
    """Get detailed user information"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get user's prediction count
    prediction_count = Prediction.query.filter_by(user_id=user_id).count()
    
    # Get recent predictions
    recent_predictions = Prediction.query.filter_by(user_id=user_id)\
        .order_by(desc(Prediction.created_at))\
        .limit(10)\
        .all()
    
    return jsonify({
        'user': user.to_dict(),
        'prediction_count': prediction_count,
        'recent_predictions': [p.to_dict() for p in recent_predictions]
    }), 200


@admin_bp.route('/admin/users/<int:user_id>/toggle-status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    """Activate or deactivate user account"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent admin from deactivating themselves
    if user.id == request.current_user['user_id']:
        return jsonify({'error': 'Cannot deactivate your own account'}), 400
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    return jsonify({
        'message': f'User {status} successfully',
        'user': user.to_dict()
    }), 200


@admin_bp.route('/admin/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    """Update user role (user/admin)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json(silent=True)
    if not data or 'role' not in data:
        return jsonify({'error': 'Role is required'}), 422
    
    role = data['role']
    if role not in ['user', 'admin']:
        return jsonify({'error': 'Invalid role. Must be "user" or "admin"'}), 422
    
    # Prevent admin from demoting themselves
    if user.id == request.current_user['user_id'] and role == 'user':
        return jsonify({'error': 'Cannot change your own role'}), 400
    
    user.role = role
    db.session.commit()
    
    return jsonify({
        'message': f'User role updated to {role}',
        'user': user.to_dict()
    }), 200


@admin_bp.route('/admin/stats', methods=['GET'])
@admin_required
def get_system_stats():
    """Get system-wide statistics"""
    
    # User statistics
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    admin_users = User.query.filter_by(role='admin').count()
    
    # Prediction statistics
    total_predictions = Prediction.query.count()
    predictions_today = Prediction.query.filter(
        func.date(Prediction.created_at) == func.current_date()
    ).count()
    
    # Prediction distribution
    prediction_distribution = db.session.query(
        Prediction.prediction,
        func.count(Prediction.id).label('count')
    ).group_by(Prediction.prediction).all()
    
    # Recent activity
    recent_predictions = Prediction.query\
        .order_by(desc(Prediction.created_at))\
        .limit(10)\
        .all()
    
    # Top users by prediction count
    top_users = db.session.query(
        User.id,
        User.username,
        User.full_name,
        func.count(Prediction.id).label('prediction_count')
    ).join(Prediction).group_by(User.id)\
     .order_by(desc('prediction_count'))\
     .limit(5)\
     .all()
    
    return jsonify({
        'users': {
            'total': total_users,
            'active': active_users,
            'admins': admin_users
        },
        'predictions': {
            'total': total_predictions,
            'today': predictions_today,
            'distribution': {item[0]: item[1] for item in prediction_distribution}
        },
        'recent_activity': [p.to_dict() for p in recent_predictions],
        'top_users': [
            {
                'id': u[0],
                'username': u[1],
                'full_name': u[2],
                'prediction_count': u[3]
            } for u in top_users
        ]
    }), 200


@admin_bp.route('/admin/predictions', methods=['GET'])
@admin_required
def get_all_predictions():
    """Get all predictions with filters"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    prediction_type = request.args.get('type')  # High, Medium, Low
    user_id = request.args.get('user_id', type=int)
    
    query = Prediction.query
    
    if prediction_type:
        query = query.filter_by(prediction=prediction_type)
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    pagination = query.order_by(desc(Prediction.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'predictions': [p.to_dict() for p in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
    }), 200


@admin_bp.route('/admin/predictions/<int:prediction_id>', methods=['DELETE'])
@admin_required
def delete_prediction(prediction_id):
    """Delete a prediction record"""
    prediction = Prediction.query.get(prediction_id)
    if not prediction:
        return jsonify({'error': 'Prediction not found'}), 404
    
    try:
        db.session.delete(prediction)
        db.session.commit()
        return jsonify({'message': 'Prediction deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500
