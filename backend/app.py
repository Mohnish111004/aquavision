import os
import joblib
import warnings
warnings.filterwarnings("ignore", category=UserWarning)   # suppress sklearn version warnings

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database
from database import init_db

# Import routes
from routes.predict   import predict_bp
from routes.health    import health_bp
from routes.metrics   import metrics_bp
from routes.explain   import explain_bp
from routes.forecast  import forecast_bp
from routes.recommend import recommend_bp
from routes.auth      import auth_bp
from routes.admin     import admin_bp
from routes.weather   import weather_bp
from routes.crops     import crops_bp
from routes.history   import history_bp
from routes.reports   import reports_bp
from routes.models    import models_bp

# ── App factory ──────────────────────────────────────────────────────────────
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aquavision-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aquavision.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

# CORS configuration
CORS(app, origins=["http://localhost:5173", "http://localhost:3000", "*"])

# Initialize database
db = init_db(app)

# ── Load model at startup ─────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "aquavision_model.joblib")

model_store = {"clf": None, "payload": None}

if os.path.exists(MODEL_PATH):
    payload = joblib.load(MODEL_PATH)
    model_store["clf"]     = payload["model"]
    model_store["payload"] = payload
    print(f"✅ Model loaded: {payload.get('model_name', 'Unknown')} from {MODEL_PATH}")
else:
    print(f"⚠️  Model file not found at {MODEL_PATH}. Run: python3 model/train_model.py")

# Pass model store to blueprints via app config
app.config["MODEL_STORE"] = model_store

# ── Register blueprints ───────────────────────────────────────────────────────
# Core prediction routes
app.register_blueprint(predict_bp)
app.register_blueprint(health_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(explain_bp)
app.register_blueprint(forecast_bp)
app.register_blueprint(recommend_bp)

# New feature routes
app.register_blueprint(auth_bp)        # Authentication
app.register_blueprint(admin_bp)       # Admin panel
app.register_blueprint(weather_bp)     # Weather API
app.register_blueprint(crops_bp)       # Crop & irrigation recommendations
app.register_blueprint(history_bp)     # Prediction history
app.register_blueprint(reports_bp)     # PDF reports
app.register_blueprint(models_bp)      # Model comparison

print("\n" + "=" * 70)
print("🚀 AquaVision AI Backend Server")
print("=" * 70)
print("✅ Database initialized")
print("✅ All routes registered")
print("📍 Server running on http://localhost:5001")
print("=" * 70 + "\n")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
