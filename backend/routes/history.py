"""
Prediction history routes
"""
from flask import Blueprint, request, jsonify
from sqlalchemy import desc
from datetime import datetime
from database import db
from database.models import Prediction
from utils.auth import token_required, optional_auth

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
@token_required
def get_user_history():
    """Get prediction history for current user"""
    user_id = request.current_user['user_id']
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    prediction_type = request.args.get('type')  # Filter by High/Medium/Low
    
    query = Prediction.query.filter_by(user_id=user_id)
    
    if prediction_type:
        query = query.filter_by(prediction=prediction_type)
    
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


@history_bp.route('/history/<int:prediction_id>', methods=['GET'])
@token_required
def get_prediction_detail(prediction_id):
    """Get detailed information about a specific prediction"""
    user_id = request.current_user['user_id']
    
    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=user_id
    ).first()
    
    if not prediction:
        return jsonify({'error': 'Prediction not found'}), 404
    
    return jsonify({'prediction': prediction.to_dict()}), 200


@history_bp.route('/history', methods=['POST'])
@token_required
def save_prediction():
    """Save a new prediction to history"""
    user_id = request.current_user['user_id']
    data = request.get_json(silent=True)
    
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # Validate required fields
    required = ['latitude', 'longitude', 'currentlevel', 'level_diff', 
                'date', 'prediction', 'confidence']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({'error': 'Missing required fields', 'missing': missing}), 422
    
    try:
        # Parse date
        prediction_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        # Create prediction record
        prediction = Prediction(
            user_id=user_id,
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            currentlevel=float(data['currentlevel']),
            level_diff=float(data['level_diff']),
            date=prediction_date,
            state_name=data.get('state_name'),
            district_name=data.get('district_name'),
            basin=data.get('basin'),
            sub_basin=data.get('sub_basin'),
            station_name=data.get('station_name'),
            prediction=data['prediction'],
            confidence=float(data['confidence']),
            current_status=data.get('current_status'),
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            rainfall=data.get('rainfall'),
            weather_condition=data.get('weather_condition'),
            model_version=data.get('model_version', 'v1.0')
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        return jsonify({
            'message': 'Prediction saved successfully',
            'prediction': prediction.to_dict()
        }), 201
    
    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 422
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to save prediction: {str(e)}'}), 500


@history_bp.route('/history/<int:prediction_id>', methods=['DELETE'])
@token_required
def delete_prediction(prediction_id):
    """Delete a prediction from history"""
    user_id = request.current_user['user_id']
    
    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=user_id
    ).first()
    
    if not prediction:
        return jsonify({'error': 'Prediction not found'}), 404
    
    try:
        db.session.delete(prediction)
        db.session.commit()
        return jsonify({'message': 'Prediction deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500


@history_bp.route('/history/stats', methods=['GET'])
@token_required
def get_user_stats():
    """Get statistics for current user's predictions"""
    user_id = request.current_user['user_id']
    
    # Total predictions
    total = Prediction.query.filter_by(user_id=user_id).count()
    
    # Prediction distribution
    from sqlalchemy import func
    distribution = db.session.query(
        Prediction.prediction,
        func.count(Prediction.id).label('count')
    ).filter_by(user_id=user_id).group_by(Prediction.prediction).all()
    
    # Recent predictions
    recent = Prediction.query.filter_by(user_id=user_id)\
        .order_by(desc(Prediction.created_at))\
        .limit(5)\
        .all()
    
    # Average confidence
    avg_confidence = db.session.query(
        func.avg(Prediction.confidence)
    ).filter_by(user_id=user_id).scalar()
    
    return jsonify({
        'total_predictions': total,
        'distribution': {item[0]: item[1] for item in distribution},
        'average_confidence': round(float(avg_confidence), 2) if avg_confidence else 0,
        'recent_predictions': [p.to_dict() for p in recent]
    }), 200
