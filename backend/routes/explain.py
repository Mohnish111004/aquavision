"""
XAI (Explainable AI) endpoint.
Generates human-readable feature contributions and natural-language explanation
without requiring SHAP (which has heavy dependencies).
Uses the model's feature importances × input deviation from typical values.
"""
from flask import Blueprint, request, jsonify, current_app
import pandas as pd
import numpy as np

explain_bp = Blueprint("explain", __name__)

# Typical (median) reference values for each feature
REFERENCE = {
    "latitude":     23.5,
    "longitude":    80.0,
    "currentlevel": 5.7,
    "level_diff":   0.0,
    "year":         2022,
    "month":        6,
    "day":          15,
    "dayofyear":    166,
}

FEATURE_LABELS = {
    "currentlevel":          "Groundwater Level",
    "level_diff":            "Level Change",
    "latitude":              "Latitude",
    "longitude":             "Longitude",
    "month":                 "Month",
    "dayofyear":             "Day of Year",
    "year":                  "Year",
    "day":                   "Day",
    "state_name_encoded":    "State",
    "district_name_encoded": "District",
    "basin_encoded":         "River Basin",
    "sub_basin_encoded":     "Sub Basin",
    "station_name_encoded":  "Station",
}


def _build_explanation(prediction: str, confidence: float,
                       input_df: pd.DataFrame, importances: list,
                       features: list) -> dict:
    """
    Build feature contributions and a natural-language explanation.
    """
    # Normalise importances
    imp_arr = np.array(importances)
    imp_arr = imp_arr / imp_arr.sum()

    contributions = []
    for feat, imp in zip(features, imp_arr):
        val = float(input_df[feat].iloc[0])
        ref = REFERENCE.get(feat, val)
        deviation = abs(val - ref) / (abs(ref) + 1e-6)
        score = float(imp * (1 + deviation))
        contributions.append({
            "feature": FEATURE_LABELS.get(feat, feat),
            "value":   round(val, 3),
            "importance": round(float(imp), 4),
            "contribution": round(score, 4),
        })

    # Sort by contribution descending
    contributions.sort(key=lambda x: x["contribution"], reverse=True)
    top3 = contributions[:3]

    # Natural-language explanation
    level = float(input_df["currentlevel"].iloc[0])
    diff  = float(input_df["level_diff"].iloc[0])

    if prediction == "High":
        level_desc = "shallow groundwater depth" if level <= 3.65 else "moderate groundwater depth"
        trend_desc = "stable or rising water table" if diff <= 0 else "slight decline"
        summary = (
            f"The model predicts HIGH water availability with {confidence:.1f}% confidence. "
            f"Key factors: {level_desc} ({level:.2f}m), {trend_desc} (Δ{diff:+.2f}m), "
            f"and strong regional patterns from {top3[2]['feature']}. "
            f"Conditions are favourable for irrigation and water use."
        )
    elif prediction == "Medium":
        summary = (
            f"The model predicts MEDIUM water availability with {confidence:.1f}% confidence. "
            f"Groundwater depth is {level:.2f}m — within the moderate range (3.65–7.76m). "
            f"Level change of {diff:+.2f}m suggests {'improving' if diff < 0 else 'declining'} conditions. "
            f"Monitor usage and consider conservation measures."
        )
    else:
        summary = (
            f"The model predicts LOW water availability with {confidence:.1f}% confidence. "
            f"Groundwater depth of {level:.2f}m exceeds the critical threshold (7.76m). "
            f"Level change of {diff:+.2f}m indicates {'worsening' if diff > 0 else 'stabilising'} depletion. "
            f"Immediate water conservation and alternative sourcing is strongly recommended."
        )

    return {
        "summary": summary,
        "top_features": top3,
        "all_contributions": contributions,
    }


@explain_bp.route("/explain", methods=["POST"])
def explain():
    model_store = current_app.config["MODEL_STORE"]
    clf     = model_store["clf"]
    payload = model_store["payload"]

    if clf is None:
        return jsonify({"error": "Model not loaded."}), 503

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    try:
        from routes.predict import REQUIRED_FIELDS, NUMERIC_FIELDS
        label_mappings = payload["label_mappings"]
        features       = payload["features"]
        class_names    = payload["class_names"]

        date = pd.to_datetime(data.get("date", pd.Timestamp.now().strftime("%Y-%m-%d")))

        def encode(col, val):
            return label_mappings.get(col, {}).get("mapping", {}).get(val, 0)

        input_df = pd.DataFrame([[
            float(data["latitude"]),
            float(data["longitude"]),
            float(data["currentlevel"]),
            float(data["level_diff"]),
            date.year, date.month, date.day, date.dayofyear,
            encode("state_name",    data.get("state_name", "")),
            encode("district_name", data.get("district_name", "")),
            encode("basin",         data.get("basin", "")),
            encode("sub_basin",     data.get("sub_basin", "")),
            encode("station_name",  data.get("station_name", "")),
        ]], columns=features)

        pred_idx = clf.predict(input_df)[0]
        probs    = clf.predict_proba(input_df)[0]
        prediction = class_names[pred_idx]
        confidence = float(probs[pred_idx] * 100)

        # Get feature importances from model
        if hasattr(clf, "feature_importances_"):
            importances = clf.feature_importances_.tolist()
        else:
            importances = [1 / len(features)] * len(features)

        explanation = _build_explanation(
            prediction, confidence, input_df, importances, features
        )

        return jsonify({
            "prediction":  prediction,
            "confidence":  round(confidence, 2),
            "explanation": explanation,
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
