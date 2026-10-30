from flask import Flask, request, jsonify
import json

app = Flask(__name__)
REPORT_FILE = "test-report.json"

@app.route("/", methods=["GET"])
def health():
    return jsonify({"service": "report receiver", "endpoint": "POST /report"})

@app.route("/report", methods=["POST"])
def receive_report():
    data = request.get_json(force=True, silent=True)
    if data is None:
        body = request.get_data(as_text=True)
        print("[rejected] Content-Type:", request.content_type, "| body:", body[:200])
        return jsonify({"error": "Invalid JSON", "content_type": request.content_type}), 400

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("[saved]", REPORT_FILE, "-", data.get("overall_status"), data.get("commit_sha"))
    return jsonify({"status": "success", "message": "Report saved"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)