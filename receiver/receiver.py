from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
REPORT_FILE = "test-report.json"

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload received"}), 400
    
    with open(REPORT_FILE, "w") as f:
        json.dump(data, f, indent=4)
        
    print("Test report successfully received and saved to", REPORT_FILE)
    return jsonify({"status": "success", "message": "Report saved"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
