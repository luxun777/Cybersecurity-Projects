from flask import Flask, render_template, request, jsonify
from utils.password_checker import evaluate_password, generate_strong_password
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({
            "score": 0,
            "strength": "Empty",
            "suggestions": ["Please enter a password."]
        })
        
    result = evaluate_password(password)
    return jsonify(result)
@app.route('/generate', methods=['GET'])
def generate():
    password = generate_strong_password()
    return jsonify({"password": password})
if __name__ == '__main__':
    app.run(debug=True, port=5000)
