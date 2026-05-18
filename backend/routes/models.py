"""
Model comparison and analysis routes
"""
from flask import Blueprint, jsonify
import os
import joblib

models_bp = Blueprint('models', __name__)

@models_bp.route('/models/comparison', methods=['GET'])
def get_model_comparison():
    """Get comparative analysis results of all trained models"""
    
    comparison_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'output',
        'model_comparison.joblib'
    )
    
    if not os.path.exists(comparison_path):
        return jsonify({
            'error': 'Model comparison data not found',
            'hint': 'Run: python3 backend/model/compare_models.py'
        }), 404
    
    try:
        comparison_data = joblib.load(comparison_path)
        
        # Format results for API response
        models_summary = []
        for model_name, metrics in comparison_data['results'].items():
            if 'error' not in metrics:
                models_summary.append({
                    'name': model_name,
                    'accuracy': round(metrics['accuracy'], 4),
                    'precision': round(metrics['precision'], 4),
                    'recall': round(metrics['recall'], 4),
                    'f1_score': round(metrics['f1_score'], 4),
                    'cv_mean': round(metrics['cv_mean'], 4),
                    'cv_std': round(metrics['cv_std'], 4),
                    'is_best': model_name == comparison_data['best_model']
                })
        
        # Sort by accuracy
        models_summary.sort(key=lambda x: x['accuracy'], reverse=True)
        
        return jsonify({
            'timestamp': comparison_data['timestamp'],
            'best_model': comparison_data['best_model'],
            'models': models_summary,
            'class_names': comparison_data['class_names'],
            'total_models': len(models_summary)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to load comparison data: {str(e)}'}), 500


@models_bp.route('/models/comparison/<model_name>', methods=['GET'])
def get_model_details(model_name):
    """Get detailed metrics for a specific model"""
    
    comparison_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'output',
        'model_comparison.joblib'
    )
    
    if not os.path.exists(comparison_path):
        return jsonify({'error': 'Model comparison data not found'}), 404
    
    try:
        comparison_data = joblib.load(comparison_path)
        
        if model_name not in comparison_data['results']:
            return jsonify({'error': f'Model "{model_name}" not found'}), 404
        
        metrics = comparison_data['results'][model_name]
        
        if 'error' in metrics:
            return jsonify({
                'model_name': model_name,
                'error': metrics['error']
            }), 500
        
        return jsonify({
            'model_name': model_name,
            'is_best': model_name == comparison_data['best_model'],
            'metrics': {
                'accuracy': round(metrics['accuracy'], 4),
                'precision': round(metrics['precision'], 4),
                'recall': round(metrics['recall'], 4),
                'f1_score': round(metrics['f1_score'], 4),
                'cv_mean': round(metrics['cv_mean'], 4),
                'cv_std': round(metrics['cv_std'], 4)
            },
            'confusion_matrix': metrics['confusion_matrix'],
            'class_names': comparison_data['class_names']
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to load model details: {str(e)}'}), 500


@models_bp.route('/models/current', methods=['GET'])
def get_current_model():
    """Get information about the currently loaded model"""
    from flask import current_app
    
    model_store = current_app.config.get("MODEL_STORE", {})
    payload = model_store.get("payload")
    
    if not payload:
        return jsonify({
            'error': 'No model currently loaded',
            'hint': 'Run: python3 backend/model/train_model.py'
        }), 404
    
    return jsonify({
        'model_name': payload.get('model_name', 'Unknown'),
        'accuracy': payload.get('accuracy'),
        'trained_at': payload.get('trained_at'),
        'features': payload.get('features'),
        'class_names': payload.get('class_names'),
        'thresholds': payload.get('thresholds')
    }), 200
