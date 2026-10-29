from flask import Flask, request, jsonify, send_from_directory
import os
from app.validation import validate_submission
from app.storage import get_submissions, save_submission

app = Flask(__name__, static_folder="../public", static_url_path="")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/submissions", methods=["GET"])
def list_submissions():
    return jsonify(get_submissions()), 200

@app.route("/api/submissions", methods=["POST"])
def create_submission():
    data = request.get_json()
    is_valid, msg = validate_submission(data)
    if not is_valid:
        return jsonify({"message": msg}), 400
    
    save_submission(data)
    return jsonify({"message": "Submission saved successfully"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
