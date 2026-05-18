"""
7-day water availability forecast endpoint.
Uses the trained model to simulate a 7-day forward projection
by incrementally adjusting the groundwater level based on
seasonal patterns and the observed level_diff trend.
"""
from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

forecast_bp = Blueprint("forecast", __name__)

# Seasonal adjustment factors (month → daily drift in metres)
SEASONAL_DRIFT = {
    1: +0.02, 2: +0.03, 3: +0.04, 4: +0.05,   # dry season — rising depth
    5: +0.06, 6: -0.02, 7: -0.08, 8: -0.10,   # monsoon onset — falling depth
    9: -0.06, 10: -0.03, 11: +0.01, 12: +0.02,
}


@forecast_bp.route("/forecast", methods=["POST"])
def forecast():
    model_store = current_app.config["MODEL_STORE"]
    clf     = model_store["clf"]
    payload = model_store["payload"]

    if clf is None:
        return jsonify({"error": "Model not loaded."}), 503

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    try:
        label_mappings = payload["label_mappings"]
        features       = payload["features"]
        class_names    = payload["class_names"]
        thresholds     = payload.get("thresholds", {"low_limit": 3.65, "medium_limit": 7.76})

        base_date  = pd.to_datetime(data.get("date", pd.Timestamp.now().strftime("%Y-%m-%d")))
        base_level = float(data.get("currentlevel", 5.0))
        level_diff = float(data.get("level_diff", 0.0))

        def encode(col, val):
            return label_mappings.get(col, {}).get("mapping", {}).get(val, 0)

        state_enc    = encode("state_name",    data.get("state_name", ""))
        district_enc = encode("district_name", data.get("district_name", ""))
        basin_enc    = encode("basin",         data.get("basin", ""))
        sub_enc      = encode("sub_basin",     data.get("sub_basin", ""))
        station_enc  = encode("station_name",  data.get("station_name", ""))

        results = []
        current_level = base_level
        current_diff  = level_diff

        for day_offset in range(7):
            forecast_date = base_date + timedelta(days=day_offset + 1)
            month = forecast_date.month

            # Simulate level change: trend + seasonal + small noise
            seasonal = SEASONAL_DRIFT.get(month, 0.0)
            noise    = np.random.normal(0, 0.05)
            delta    = (current_diff * 0.6) + (seasonal * 0.4) + noise
            new_level = max(0.5, current_level + delta)

            row = pd.DataFrame([[
                float(data.get("latitude", 23.5)),
                float(data.get("longitude", 80.0)),
                new_level,
                delta,
                forecast_date.year, forecast_date.month,
                forecast_date.day, forecast_date.dayofyear,
                state_enc, district_enc, basin_enc, sub_enc, station_enc,
            ]], columns=features)

            pred_idx   = clf.predict(row)[0]
            probs      = clf.predict_proba(row)[0]
            prediction = class_names[pred_idx]
            confidence = round(float(probs[pred_idx] * 100), 1)

            results.append({
                "date":        forecast_date.strftime("%Y-%m-%d"),
                "day":         forecast_date.strftime("%a"),
                "level":       round(new_level, 2),
                "prediction":  prediction,
                "confidence":  confidence,
                "probabilities": {
                    class_names[i]: round(float(probs[i]) * 100, 1)
                    for i in range(len(class_names))
                },
            })

            current_diff  = delta
            current_level = new_level

        return jsonify({
            "base_date":  base_date.strftime("%Y-%m-%d"),
            "base_level": base_level,
            "forecast":   results,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
