"""
Database models for AquaVision AI
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    predictions = db.relationship('Prediction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }


class Prediction(db.Model):
    """Prediction history model"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Input parameters
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    currentlevel = db.Column(db.Float, nullable=False)
    level_diff = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    state_name = db.Column(db.String(100))
    district_name = db.Column(db.String(100))
    basin = db.Column(db.String(100))
    sub_basin = db.Column(db.String(100))
    station_name = db.Column(db.String(100))
    
    # Prediction results
    prediction = db.Column(db.String(20), nullable=False)  # High, Medium, Low
    confidence = db.Column(db.Float, nullable=False)
    current_status = db.Column(db.String(20))
    
    # Weather data (if available)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    rainfall = db.Column(db.Float)
    weather_condition = db.Column(db.String(50))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    model_version = db.Column(db.String(50))
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'currentlevel': self.currentlevel,
            'level_diff': self.level_diff,
            'date': self.date.isoformat() if self.date else None,
            'state_name': self.state_name,
            'district_name': self.district_name,
            'basin': self.basin,
            'sub_basin': self.sub_basin,
            'station_name': self.station_name,
            'prediction': self.prediction,
            'confidence': self.confidence,
            'current_status': self.current_status,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'rainfall': self.rainfall,
            'weather_condition': self.weather_condition,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'model_version': self.model_version
        }


class SystemMetrics(db.Model):
    """System metrics and statistics"""
    __tablename__ = 'system_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(100), nullable=False, index=True)
    metric_value = db.Column(db.Float, nullable=False)
    metric_data = db.Column(db.JSON)  # For storing complex data
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_data': self.metric_data,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }
