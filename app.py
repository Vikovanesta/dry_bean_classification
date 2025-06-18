from flask import Flask, request, render_template, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Config
MODEL_FILENAME = "dry_bean_rf_s.joblib"
SCALER_FILENAME = "scaler.joblib"
CLASS_NAMES = ["Barbunya", "Bombay", "Cali", "Dermason", "Horoz", "Seker", "Sira"]
EXPECTED_FEATURE_NAMES = [
    'Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength', 'AspectRation',
    'Eccentricity', 'ConvexArea', 'EquivDiameter', 'Extent', 'Solidity',
    'roundness', 'Compactness', 'ShapeFactor1', 'ShapeFactor2', 'ShapeFactor3', 'ShapeFactor4'
]

# Range value buat form randomizer
FEATURE_RANGES_PY = {
    'Area': (20000, 250000, 0), 'Perimeter': (500, 2000, 2),
    'MajorAxisLength': (200, 750, 2), 'MinorAxisLength': (150, 450, 2),
    'AspectRation': (1.0, 2.5, 4), 'Eccentricity': (0.2, 0.99, 4),
    'ConvexArea': (20000, 250000, 0), 'EquivDiameter': (150, 550, 1),
    'Extent': (0.4, 0.9, 3), 'Solidity': (0.9, 0.99, 4),
    'roundness': (0.5, 0.95, 4), 'Compactness': (0.5, 0.9, 4),
    'ShapeFactor1': (0.002, 0.009, 5), 'ShapeFactor2': (0.0005, 0.0025, 6),
    'ShapeFactor3': (0.4, 0.9, 4), 'ShapeFactor4': (0.9, 0.999, 5)
}

def get_default_feature_values():
    """Calculates default values (titik tengah range) for the form."""
    defaults = {}
    for feature in EXPECTED_FEATURE_NAMES:
        min_val, max_val, decimals = FEATURE_RANGES_PY.get(feature, (0, 1, 2))
        default_val = (min_val + max_val) / 2
        defaults[feature] = round(default_val, decimals)
    return defaults

# Load model & scaler
model = None
scaler = None
load_error = None
try:
    if os.path.exists(MODEL_FILENAME):
        model = joblib.load(MODEL_FILENAME)
        print(f"Model '{MODEL_FILENAME}' has been loaded.")
    else:
        load_error = f"File model '{MODEL_FILENAME}' not found."

    if os.path.exists(SCALER_FILENAME):
        scaler = joblib.load(SCALER_FILENAME)
        print(f"Scaler '{SCALER_FILENAME}' has been loaded.")
    else:
        load_error = f"File scaler '{SCALER_FILENAME}' not found." if not load_error else load_error
        
except Exception as e:
    load_error = f"Failed to load ML model or scaler: {str(e)}"

if load_error:
    print(load_error)


# Routes
@app.route('/')
def home():
    """Render Frontend"""
    return render_template('index.html',
                           feature_names=EXPECTED_FEATURE_NAMES,
                           feature_defaults=get_default_feature_values(),
                           feature_ranges=FEATURE_RANGES_PY,
                           initial_error=load_error)


@app.route('/predict', methods=['POST'])
def predict():
    """Receives feature data as JSON and return a prediction as JSON."""
    if model is None or scaler is None:
        return jsonify({'success': False, 'error': f"Model or Scaler is not loaded. {load_error}"}), 500

    try:
        input_data = request.get_json()
        if not input_data:
            return jsonify({'success': False, 'error': 'Invalid request: No JSON data received.'}), 400

        # Validation
        input_features_dict = {}
        for feature_name in EXPECTED_FEATURE_NAMES:
            value = input_data.get(feature_name)
            if value is None or value == '':
                raise ValueError(f"Feature '{feature_name}' is missing from the request.")
            try:
                input_features_dict[feature_name] = float(value)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid input for '{feature_name}'. A numeric value is required.")

        input_df = pd.DataFrame([input_features_dict])[EXPECTED_FEATURE_NAMES]
        
        #  Apply standard scaling
        input_df = scaler.transform(input_df)

        # Predict
        prediction_idx = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]

        if not (0 <= prediction_idx < len(CLASS_NAMES)):
            raise ValueError(f"Model returned an invalid class index: {prediction_idx}.")

        predicted_bean_type = CLASS_NAMES[prediction_idx]
        probabilities_dict = {CLASS_NAMES[i]: float(prob) for i, prob in enumerate(prediction_proba)}

        return jsonify({
            'success': True,
            'prediction': predicted_bean_type,
            'probabilities': probabilities_dict
        })

    except ValueError as ve:
        return jsonify({'success': False, 'error': str(ve)}), 400
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'success': False, 'error': f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)