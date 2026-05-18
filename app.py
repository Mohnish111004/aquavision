import os
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the trained model and metadata
MODEL_PATH = "aquavision_model.joblib"
if os.path.exists(MODEL_PATH):
    model_payload = joblib.load(MODEL_PATH)
    clf = model_payload['model']
    label_mappings = model_payload['label_mappings']
    class_names = model_payload['class_names']
    features = model_payload['features']
else:
    print(f"Warning: Model file {MODEL_PATH} not found. Please train the model first.")
    clf = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not clf:
        return jsonify({'error': 'Model is not trained yet.'}), 500

    try:
        data = request.json
        
        # Parse date
        date = pd.to_datetime(data.get('date', pd.Timestamp.now().strftime('%Y-%m-%d')))
        
        # Extract features
        latitude = float(data.get('latitude', 0.0))
        longitude = float(data.get('longitude', 0.0))
        currentlevel = float(data.get('currentlevel', 0.0))
        level_diff = float(data.get('level_diff', 0.0))
        
        year = date.year
        month = date.month
        day = date.day
        dayofyear = date.dayofyear
        
        # Encode categorical features
        def encode(col_name, val):
            mapping = label_mappings.get(col_name, {}).get('mapping', {})
            return mapping.get(val, 0)
            
        state_name_encoded = encode('state_name', data.get('state_name', ''))
        district_name_encoded = encode('district_name', data.get('district_name', ''))
        basin_encoded = encode('basin', data.get('basin', ''))
        sub_basin_encoded = encode('sub_basin', data.get('sub_basin', ''))
        station_name_encoded = encode('station_name', data.get('station_name', ''))
        
        # Prepare input array in the correct order
        input_data = pd.DataFrame([[
            latitude, longitude, currentlevel, level_diff,
            year, month, day, dayofyear,
            state_name_encoded, district_name_encoded,
            basin_encoded, sub_basin_encoded, station_name_encoded
        ]], columns=features)
        
        # Predict
        prediction = clf.predict(input_data)[0]
        prediction_probs = clf.predict_proba(input_data)[0]
        
        predicted_class = class_names[prediction]
        confidence = float(prediction_probs[prediction] * 100)
        
        # Determine current availability status for UI context
        if currentlevel <= 3.65:
            current_status = 'High'
        elif currentlevel <= 7.76:
            current_status = 'Medium'
        else:
            current_status = 'Low'

        return jsonify({
            'prediction': predicted_class,
            'confidence': f"{confidence:.2f}%",
            'current_status': current_status,
            'probabilities': {
                class_names[i]: float(prediction_probs[i]) for i in range(len(class_names))
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
