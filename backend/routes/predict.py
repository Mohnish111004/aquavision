from flask import Blueprint, request, jsonify, current_app
import pandas as pd

predict_bp = Blueprint("predict", __name__)

REQUIRED_FIELDS = [
    "latitude", "longitude", "currentlevel", "level_diff",
    "date", "state_name", "district_name", "basin", "sub_basin", "station_name"
]

NUMERIC_FIELDS = ["latitude", "longitude", "currentlevel", "level_diff"]


@predict_bp.route("/predict", methods=["POST"])
def predict():
    model_store = current_app.config["MODEL_STORE"]
    clf = model_store["clf"]
    payload = model_store["payload"]

    # ── 503 if model not loaded ───────────────────────────────────────────────
    if clf is None:
        return jsonify({
            "error": "Model not loaded. Please train the model first.",
            "hint": "Run: python backend/model/train_model.py"
        }), 503

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    # ── Input validation ──────────────────────────────────────────────────────
    missing = [f for f in REQUIRED_FIELDS if f not in data or data[f] == ""]
    if missing:
        return jsonify({
            "error": "Missing required fields.",
            "missing_fields": missing
        }), 422

    for field in NUMERIC_FIELDS:
        try:
            float(data[field])
        except (ValueError, TypeError):
            return jsonify({
                "error": f"Field '{field}' must be a valid number.",
            }), 422

    try:
        label_mappings = payload["label_mappings"]
        features = payload["features"]
        class_names = payload["class_names"]

        # ── Parse date ────────────────────────────────────────────────────────
        date = pd.to_datetime(
            data.get("date", pd.Timestamp.now().strftime("%Y-%m-%d"))
        )

        # ── Numeric features ──────────────────────────────────────────────────
        latitude = float(data["latitude"])
        longitude = float(data["longitude"])
        currentlevel = float(data["currentlevel"])
        level_diff = float(data["level_diff"])

        year = date.year
        month = date.month
        day = date.day
        dayofyear = date.dayofyear

        # ── Categorical encoding ──────────────────────────────────────────────
        def encode(col_name, val):
            mapping = label_mappings.get(col_name, {}).get("mapping", {})
            return mapping.get(val, 0)

        state_enc = encode("state_name", data.get("state_name", ""))
        district_enc = encode("district_name", data.get("district_name", ""))
        basin_enc = encode("basin", data.get("basin", ""))
        sub_basin_enc = encode("sub_basin", data.get("sub_basin", ""))
        station_enc = encode("station_name", data.get("station_name", ""))

        # ── Build feature DataFrame ───────────────────────────────────────────
        input_df = pd.DataFrame([[
            latitude, longitude, currentlevel, level_diff,
            year, month, day, dayofyear,
            state_enc, district_enc, basin_enc, sub_basin_enc, station_enc
        ]], columns=features)

        # ── Predict ───────────────────────────────────────────────────────────
        prediction_idx = clf.predict(input_df)[0]
        probs = clf.predict_proba(input_df)[0]

        predicted_class = class_names[prediction_idx]
        confidence = float(probs[prediction_idx] * 100)

        # ── Current status from depth thresholds ──────────────────────────────
        thresholds = payload.get("thresholds", {"low_limit": 3.65, "medium_limit": 7.76})
        if currentlevel <= thresholds["low_limit"]:
            current_status = "High"
        elif currentlevel <= thresholds["medium_limit"]:
            current_status = "Medium"
        else:
            current_status = "Low"

        return jsonify({
            "prediction": predicted_class,
            "confidence": round(confidence, 2),
            "confidence_label": f"{confidence:.2f}%",
            "current_status": current_status,
            "probabilities": {
                class_names[i]: round(float(probs[i]) * 100, 2)
                for i in range(len(class_names))
            },
            "input_summary": {
                "currentlevel": currentlevel,
                "level_diff": level_diff,
                "date": str(date.date()),
                "state": data.get("state_name"),
                "district": data.get("district_name"),
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400
