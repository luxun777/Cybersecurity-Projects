from flask import Flask, render_template, request, jsonify, send_file
import os
from scanner import VulnerabilityScanner

app = Flask(__name__)

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data or 'target' not in data:
        return jsonify({'error': 'Target is required'}), 400
    
    target = data['target']
    scanner = VulnerabilityScanner(target)
    results = scanner.run()
    
    if "error" in results:
        return jsonify(results), 400
        
    return jsonify(results)

@app.route('/report/<path:filename>')
def download_report(filename):
    # Basic directory traversal protection
    if ".." in filename or "/" in filename:
        return "Invalid filename", 400
    
    file_path = os.path.join("reports", filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "Report not found", 404

if __name__ == '__main__':
    # Use waitress for a production-ready WSGI server on Windows if needed, 
    # but run standard debug for development
    app.run(debug=True, host='0.0.0.0', port=5001)
