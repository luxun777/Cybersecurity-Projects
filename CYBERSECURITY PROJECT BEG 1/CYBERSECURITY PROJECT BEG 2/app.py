from flask import Flask, request, jsonify, render_template
import joblib
import json
import os
from utils.feature_extractor import extract_features

app = Flask(__name__)

# Load model and vectorizer
MODEL_PATH = 'model/model.pkl'
VECTORIZER_PATH = 'model/vectorizer.pkl'
METRICS_PATH = 'model/metrics.json'

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model and Vectorizer loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    vectorizer = None

try:
    with open(METRICS_PATH, 'r') as f:
        metrics = json.load(f)
except:
    metrics = {"accuracy": 0, "precision": 0, "recall": 0, "confusion_matrix": [[0,0],[0,0]]}

@app.route('/')
def index():
    return render_template('index.html', metrics=metrics)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    if not model or not vectorizer:
        return jsonify({"error": "Model not loaded properly."}), 500

    data = request.json
    text = data.get('text', '')

    if not text.strip():
        return jsonify({"error": "No text provided."}), 400

    # Extract Threat Indicators
    indicators = extract_features(text)

    # Transform text and predict
    vec_text = vectorizer.transform([text])
    prediction = model.predict(vec_text)[0] # 1 for phishing, 0 for safe
    probabilities = model.predict_proba(vec_text)[0] # [prob_safe, prob_phishing]

    prob_safe = probabilities[0]
    prob_phishing = probabilities[1]

    # Model gives result, but we can augment based on heuristic indicators if model is unsure
    if len(indicators) >= 2 and prediction == 0 and prob_phishing > 0.3:
        # Heuristic override if model is on the fence but multiple indicators exist
        prediction = 1
        confidence = 90.0
    else:
        confidence = prob_phishing * 100 if prediction == 1 else prob_safe * 100

    result = {
        "prediction": "PHISHING" if prediction == 1 else "SAFE",
        "confidence": round(confidence, 1),
        "prob_safe": round(prob_safe * 100, 1),
        "prob_phishing": round(prob_phishing * 100, 1),
        "indicators": indicators,
        "recommendation": "Do not click any links or provide credentials." if prediction == 1 else "No immediate threats detected, but always remain vigilant."
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
