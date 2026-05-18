"""
Crop recommendation system based on water availability
"""
from flask import Blueprint, request, jsonify

crops_bp = Blueprint('crops', __name__)

# Crop database with water requirements and characteristics
CROP_DATABASE = {
    "High": [
        {
            "name": "Rice (Paddy)",
            "water_requirement": "Very High",
            "season": "Kharif (Monsoon)",
            "duration": "120-150 days",
            "yield_potential": "High",
            "soil": "Clay, Loamy",
            "temperature": "20-35°C",
            "description": "Requires continuous flooding. Best suited for areas with abundant water.",
            "icon": "🌾"
        },
        {
            "name": "Sugarcane",
            "water_requirement": "Very High",
            "season": "Year-round",
            "duration": "12-18 months",
            "yield_potential": "Very High",
            "soil": "Loamy, Clay",
            "temperature": "20-35°C",
            "description": "Long-duration crop with high water demand throughout growth cycle.",
            "icon": "🎋"
        },
        {
            "name": "Banana",
            "water_requirement": "High",
            "season": "Year-round",
            "duration": "9-12 months",
            "yield_potential": "High",
            "soil": "Well-drained loamy",
            "temperature": "15-35°C",
            "description": "Requires consistent moisture. High commercial value.",
            "icon": "🍌"
        },
        {
            "name": "Vegetables (Tomato, Cabbage)",
            "water_requirement": "High",
            "season": "Rabi/Summer",
            "duration": "60-120 days",
            "yield_potential": "High",
            "soil": "Loamy, Sandy loam",
            "temperature": "15-30°C",
            "description": "Short-duration crops with good market demand.",
            "icon": "🥬"
        },
        {
            "name": "Cotton",
            "water_requirement": "High",
            "season": "Kharif",
            "duration": "150-180 days",
            "yield_potential": "Medium-High",
            "soil": "Black cotton soil",
            "temperature": "21-30°C",
            "description": "Cash crop requiring adequate moisture during flowering.",
            "icon": "🌸"
        }
    ],
    "Medium": [
        {
            "name": "Wheat",
            "water_requirement": "Medium",
            "season": "Rabi (Winter)",
            "duration": "120-150 days",
            "yield_potential": "High",
            "soil": "Loamy, Clay loam",
            "temperature": "10-25°C",
            "description": "Requires 4-6 irrigations. Staple food crop with good market.",
            "icon": "🌾"
        },
        {
            "name": "Maize (Corn)",
            "water_requirement": "Medium",
            "season": "Kharif/Rabi",
            "duration": "80-120 days",
            "yield_potential": "High",
            "soil": "Well-drained loamy",
            "temperature": "18-32°C",
            "description": "Versatile crop with moderate water needs. Good for fodder too.",
            "icon": "🌽"
        },
        {
            "name": "Soybean",
            "water_requirement": "Medium",
            "season": "Kharif",
            "duration": "90-120 days",
            "yield_potential": "Medium",
            "soil": "Well-drained loamy",
            "temperature": "20-30°C",
            "description": "Oilseed crop with nitrogen-fixing properties. Good for soil health.",
            "icon": "🫘"
        },
        {
            "name": "Sunflower",
            "water_requirement": "Medium",
            "season": "Kharif/Rabi",
            "duration": "90-120 days",
            "yield_potential": "Medium",
            "soil": "Well-drained sandy loam",
            "temperature": "20-30°C",
            "description": "Oilseed crop with moderate water requirement. Drought-tolerant.",
            "icon": "🌻"
        },
        {
            "name": "Potato",
            "water_requirement": "Medium",
            "season": "Rabi",
            "duration": "90-120 days",
            "yield_potential": "High",
            "soil": "Sandy loam, Loamy",
            "temperature": "15-25°C",
            "description": "High-value vegetable crop. Requires controlled irrigation.",
            "icon": "🥔"
        }
    ],
    "Low": [
        {
            "name": "Pearl Millet (Bajra)",
            "water_requirement": "Low",
            "season": "Kharif",
            "duration": "70-90 days",
            "yield_potential": "Medium",
            "soil": "Sandy, Sandy loam",
            "temperature": "25-35°C",
            "description": "Highly drought-tolerant. Suitable for arid regions.",
            "icon": "🌾"
        },
        {
            "name": "Sorghum (Jowar)",
            "water_requirement": "Low",
            "season": "Kharif/Rabi",
            "duration": "90-120 days",
            "yield_potential": "Medium",
            "soil": "Well-drained loamy",
            "temperature": "20-35°C",
            "description": "Drought-resistant cereal. Good for dry farming.",
            "icon": "🌾"
        },
        {
            "name": "Pulses (Chickpea, Lentil)",
            "water_requirement": "Low",
            "season": "Rabi",
            "duration": "90-150 days",
            "yield_potential": "Medium",
            "soil": "Well-drained loamy",
            "temperature": "15-30°C",
            "description": "Nitrogen-fixing legumes. Require minimal irrigation.",
            "icon": "🫘"
        },
        {
            "name": "Groundnut (Peanut)",
            "water_requirement": "Low-Medium",
            "season": "Kharif",
            "duration": "100-150 days",
            "yield_potential": "Medium",
            "soil": "Sandy loam",
            "temperature": "20-30°C",
            "description": "Oilseed crop suitable for rainfed conditions.",
            "icon": "🥜"
        },
        {
            "name": "Finger Millet (Ragi)",
            "water_requirement": "Low",
            "season": "Kharif",
            "duration": "120-150 days",
            "yield_potential": "Medium",
            "soil": "Red, Sandy loam",
            "temperature": "20-30°C",
            "description": "Highly nutritious. Excellent for water-scarce regions.",
            "icon": "🌾"
        }
    ]
}

IRRIGATION_METHODS = {
    "High": {
        "recommended": [
            {
                "method": "Flood Irrigation",
                "efficiency": "40-60%",
                "suitability": "Rice, Sugarcane",
                "description": "Traditional method where entire field is flooded. Best for paddy cultivation.",
                "pros": ["Simple", "Low cost", "Suitable for heavy soils"],
                "cons": ["High water wastage", "Labor intensive", "Waterlogging risk"],
                "icon": "💧"
            },
            {
                "method": "Sprinkler Irrigation",
                "efficiency": "70-85%",
                "suitability": "Vegetables, Cotton",
                "description": "Water sprayed through nozzles. Mimics natural rainfall.",
                "pros": ["Uniform distribution", "Suitable for uneven terrain", "Reduces labor"],
                "cons": ["High initial cost", "Energy requirement", "Wind interference"],
                "icon": "💦"
            },
            {
                "method": "Drip Irrigation",
                "efficiency": "85-95%",
                "suitability": "Banana, Vegetables",
                "description": "Water delivered directly to root zone through emitters.",
                "pros": ["Maximum efficiency", "Reduces weed growth", "Fertilizer application possible"],
                "cons": ["High cost", "Maintenance required", "Clogging issues"],
                "icon": "💧"
            }
        ],
        "schedule": "Frequent irrigation (every 2-4 days)",
        "tips": [
            "Monitor soil moisture regularly",
            "Irrigate during early morning or evening",
            "Ensure proper drainage to prevent waterlogging",
            "Use mulching to reduce evaporation"
        ]
    },
    "Medium": {
        "recommended": [
            {
                "method": "Drip Irrigation",
                "efficiency": "85-95%",
                "suitability": "All crops",
                "description": "Most efficient method. Delivers water directly to roots.",
                "pros": ["Water saving", "Precise control", "Reduced disease"],
                "cons": ["Initial investment", "Technical knowledge needed"],
                "icon": "💧"
            },
            {
                "method": "Sprinkler Irrigation",
                "efficiency": "70-85%",
                "suitability": "Wheat, Maize, Vegetables",
                "description": "Good balance between efficiency and cost.",
                "pros": ["Moderate cost", "Flexible", "Good coverage"],
                "cons": ["Energy cost", "Evaporation losses"],
                "icon": "💦"
            },
            {
                "method": "Furrow Irrigation",
                "efficiency": "50-70%",
                "suitability": "Row crops",
                "description": "Water flows through furrows between crop rows.",
                "pros": ["Low cost", "Simple operation", "No energy needed"],
                "cons": ["Moderate wastage", "Labor intensive"],
                "icon": "🌊"
            }
        ],
        "schedule": "Moderate irrigation (every 5-7 days)",
        "tips": [
            "Adopt water-efficient irrigation methods",
            "Use soil moisture sensors for precision",
            "Practice deficit irrigation during non-critical stages",
            "Implement rainwater harvesting"
        ]
    },
    "Low": {
        "recommended": [
            {
                "method": "Drip Irrigation (Critical)",
                "efficiency": "85-95%",
                "suitability": "All crops",
                "description": "Essential for water conservation in scarcity conditions.",
                "pros": ["Maximum water saving", "Crop survival", "Targeted delivery"],
                "cons": ["Cost", "Maintenance"],
                "icon": "💧"
            },
            {
                "method": "Deficit Irrigation",
                "efficiency": "Variable",
                "suitability": "Drought-tolerant crops",
                "description": "Controlled water stress during non-critical growth stages.",
                "pros": ["Water conservation", "Maintains yield", "Cost-effective"],
                "cons": ["Requires expertise", "Yield reduction risk"],
                "icon": "🌱"
            },
            {
                "method": "Rainfed Farming",
                "efficiency": "100% (no irrigation)",
                "suitability": "Millets, Pulses",
                "description": "Rely entirely on rainfall. Choose drought-resistant crops.",
                "pros": ["Zero irrigation cost", "Sustainable", "Low input"],
                "cons": ["Weather dependent", "Lower yields"],
                "icon": "🌧️"
            }
        ],
        "schedule": "Minimal irrigation (critical stages only)",
        "tips": [
            "URGENT: Implement strict water conservation",
            "Switch to drought-resistant crop varieties",
            "Use mulching extensively to retain moisture",
            "Consider crop insurance",
            "Explore alternative water sources (treated wastewater)",
            "Delay planting until water situation improves"
        ]
    }
}


@crops_bp.route('/crops/recommend', methods=['POST'])
def recommend_crops():
    """Recommend crops based on water availability"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    prediction = data.get('prediction', 'Medium')
    if prediction not in CROP_DATABASE:
        return jsonify({'error': 'Invalid prediction value'}), 422
    
    # Get additional context
    season = data.get('season', 'All')
    soil_type = data.get('soil_type', 'All')
    
    crops = CROP_DATABASE[prediction]
    
    # Filter by season if provided
    if season != 'All':
        crops = [c for c in crops if season.lower() in c['season'].lower() or 'year-round' in c['season'].lower()]
    
    return jsonify({
        'water_availability': prediction,
        'recommended_crops': crops,
        'total_recommendations': len(crops),
        'message': f'Showing {len(crops)} crop recommendations for {prediction} water availability'
    }), 200


@crops_bp.route('/irrigation/recommend', methods=['POST'])
def recommend_irrigation():
    """Recommend irrigation methods based on water availability"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400
    
    prediction = data.get('prediction', 'Medium')
    if prediction not in IRRIGATION_METHODS:
        return jsonify({'error': 'Invalid prediction value'}), 422
    
    irrigation_data = IRRIGATION_METHODS[prediction]
    
    return jsonify({
        'water_availability': prediction,
        'irrigation_methods': irrigation_data['recommended'],
        'schedule': irrigation_data['schedule'],
        'tips': irrigation_data['tips']
    }), 200
