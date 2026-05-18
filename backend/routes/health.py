from flask import Blueprint, jsonify, current_app

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health():
    model_store = current_app.config["MODEL_STORE"]
    payload = model_store.get("payload")
    model_loaded = model_store["clf"] is not None

    return jsonify({
        "status": "ok",
        "model_loaded": model_loaded,
        "model_name": payload.get("model_name") if payload else None,
    }), 200
