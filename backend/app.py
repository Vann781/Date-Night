from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.models.request import DatePlanRequest
from backend.agent.orchestrator import plan_date

app = Flask(__name__)
CORS(app)


@app.route("/api/plan-date", methods=["POST"])
def handle_plan_date():
    data = request.get_json(silent=True) or {}
    try:
        req = DatePlanRequest(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    try:
        result = plan_date(req)
        return jsonify(result.model_dump()), 200
    except Exception as e:
        return jsonify({"error": f"Agent error: {str(e)}"}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
