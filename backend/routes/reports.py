"""
PDF Report generation routes
"""
from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
import io
from utils.pdf_generator import generate_prediction_report
from utils.auth import token_required, optional_auth
from database.models import User, Prediction

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports/generate', methods=['POST'])
@optional_auth
def generate_report():
    """Generate PDF report for a prediction"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    # Get user info if authenticated
    user_info = None
    if hasattr(request, 'current_user') and request.current_user:
        user = User.query.get(request.current_user['user_id'])
        if user:
            user_info = user.to_dict()
    
    try:
        # Generate PDF
        pdf_data = generate_prediction_report(data, user_info)
        
        # Create file buffer
        buffer = io.BytesIO(pdf_data)
        buffer.seek(0)
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"AquaVision_Report_{timestamp}.pdf"
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500


@reports_bp.route('/reports/history/<int:prediction_id>', methods=['GET'])
@token_required
def generate_history_report(prediction_id):
    """Generate PDF report from saved prediction history"""
    user_id = request.current_user['user_id']
    
    # Get prediction from database
    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=user_id
    ).first()
    
    if not prediction:
        return jsonify({'error': 'Prediction not found'}), 404
    
    # Get user info
    user = User.query.get(user_id)
    user_info = user.to_dict() if user else None
    
    try:
        # Convert prediction to dict for report
        prediction_data = prediction.to_dict()
        
        # Generate PDF
        pdf_data = generate_prediction_report(prediction_data, user_info)
        
        # Create file buffer
        buffer = io.BytesIO(pdf_data)
        buffer.seek(0)
        
        # Generate filename
        filename = f"AquaVision_Report_{prediction_id}.pdf"
        
        return send_file(
            buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500
