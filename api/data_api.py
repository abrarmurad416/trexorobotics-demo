"""
Trexo Robotics Data API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime, timedelta
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

API_KEYS = {
    "demo_key_123": "readonly",
    "admin_key_456": "admin"
}

def require_api_key(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get("X-API-Key") or request.args.get("api_key")
        if not api_key or api_key not in API_KEYS:
            return jsonify({"error": "Invalid or missing API key"}), 401
        return f(*args, **kwargs)
    return wrapper


class DataWarehouse:
    def get_device_usage_stats(self, start_date=None, end_date=None, device_id=None):
        return {
            "total_sessions": 1250,
            "total_steps": 450000,
            "total_distance_km": 320.5,
            "active_devices": 45,
            "active_patients": 120,
            "avg_session_duration_minutes": 35,
            "date_range": {
                "start": start_date or (datetime.now() - timedelta(days=30)).isoformat(),
                "end": end_date or datetime.now().isoformat()
            }
        }

    def get_patient_outcomes(self):
        return {
            "total_patients": 150,
            "avg_walking_improvement": 25.5,
            "avg_mobility_improvement": 18.3,
            "high_independence_count": 45,
            "improvement_rate": 0.75
        }

    def get_device_reliability(self):
        return {
            "total_devices": 50,
            "active_devices": 45,
            "avg_error_rate": 0.02,
            "devices_needing_attention": 2,
            "reliability_score": 0.98
        }


dw = DataWarehouse()

@app.route("/")
def home():
    return "Trexo Robotics API running 🚀"

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route("/api/dashboard-summary", methods=["GET"])
@require_api_key
def dashboard_summary():
    summary = {
        "device_usage": dw.get_device_usage_stats(),
        "patient_outcomes": dw.get_patient_outcomes(),
        "device_reliability": dw.get_device_reliability(),
        "timestamp": datetime.now().isoformat()
    }
    return jsonify({"success": True, "data": summary})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
