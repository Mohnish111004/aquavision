"""
AI Recommendation engine.
Returns context-aware water management recommendations
based on prediction result, confidence, and input parameters.
"""
from flask import Blueprint, request, jsonify

recommend_bp = Blueprint("recommend", __name__)

RECOMMENDATIONS = {
    "High": [
        {
            "category": "Irrigation",
            "priority": "low",
            "title":    "Optimal Irrigation Window",
            "detail":   "Water table is healthy. Schedule irrigation during early morning (5–8 AM) to minimise evaporation losses.",
            "icon":     "droplets",
        },
        {
            "category": "Storage",
            "priority": "low",
            "title":    "Recharge Groundwater",
            "detail":   "Favourable conditions for rainwater harvesting. Install percolation pits to recharge the aquifer for dry seasons.",
            "icon":     "archive",
        },
        {
            "category": "Agriculture",
            "priority": "low",
            "title":    "Crop Planning",
            "detail":   "High availability supports water-intensive crops. Consider paddy, sugarcane, or vegetables this season.",
            "icon":     "leaf",
        },
        {
            "category": "Monitoring",
            "priority": "info",
            "title":    "Continue Monitoring",
            "detail":   "Maintain weekly groundwater level readings to detect early signs of depletion before the dry season.",
            "icon":     "activity",
        },
    ],
    "Medium": [
        {
            "category": "Conservation",
            "priority": "medium",
            "title":    "Reduce Non-Essential Usage",
            "detail":   "Limit water use for non-agricultural purposes. Fix leaks and avoid over-irrigation.",
            "icon":     "alert-triangle",
        },
        {
            "category": "Irrigation",
            "priority": "medium",
            "title":    "Switch to Drip Irrigation",
            "detail":   "Drip systems reduce water consumption by 40–60% compared to flood irrigation. Prioritise for high-value crops.",
            "icon":     "droplets",
        },
        {
            "category": "Storage",
            "priority": "medium",
            "title":    "Build Water Reserves",
            "detail":   "Construct farm ponds or check dams to store surface runoff before the dry season begins.",
            "icon":     "archive",
        },
        {
            "category": "Agriculture",
            "priority": "medium",
            "title":    "Drought-Tolerant Crops",
            "detail":   "Consider shifting to millets, pulses, or drought-resistant varieties to reduce water demand.",
            "icon":     "leaf",
        },
    ],
    "Low": [
        {
            "category": "Emergency",
            "priority": "critical",
            "title":    "Activate Water Rationing",
            "detail":   "Critical scarcity detected. Implement strict water rationing immediately. Prioritise drinking water over irrigation.",
            "icon":     "alert-circle",
        },
        {
            "category": "Alternative Sources",
            "priority": "critical",
            "title":    "Explore Alternative Sources",
            "detail":   "Contact local authorities for tanker supply. Explore treated wastewater reuse for non-potable applications.",
            "icon":     "refresh-cw",
        },
        {
            "category": "Agriculture",
            "priority": "high",
            "title":    "Suspend Water-Intensive Crops",
            "detail":   "Avoid planting paddy, sugarcane, or other high-water crops. Focus on drought-resistant varieties only.",
            "icon":     "x-circle",
        },
        {
            "category": "Infrastructure",
            "priority": "high",
            "title":    "Repair and Seal Infrastructure",
            "detail":   "Inspect all pipelines, canals, and storage tanks for leaks. Every litre saved is critical at this stage.",
            "icon":     "tool",
        },
    ],
}

RISK_CONFIG = {
    "High":   {"level": "Safe",            "score": 15, "color": "green",  "message": "Water resources are adequate. Normal operations can continue."},
    "Medium": {"level": "Moderate Risk",   "score": 55, "color": "amber",  "message": "Water stress is developing. Conservation measures recommended."},
    "Low":    {"level": "Critical Scarcity","score": 90, "color": "red",   "message": "Severe water scarcity. Immediate action required."},
}


@recommend_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body must be JSON."}), 400

    prediction = data.get("prediction", "Medium")
    if prediction not in RECOMMENDATIONS:
        return jsonify({"error": f"Invalid prediction value: {prediction}"}), 422

    risk = RISK_CONFIG.get(prediction, RISK_CONFIG["Medium"])

    return jsonify({
        "prediction":      prediction,
        "risk":            risk,
        "recommendations": RECOMMENDATIONS[prediction],
    }), 200
