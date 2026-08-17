import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

try:
    import analytics
except ImportError:
    analytics = None

app = Flask(__name__, static_folder="webapp", static_url_path="")
CORS(app)

@app.route("/")
def index():
    return send_from_directory("webapp", "index.html")

@app.route("/api/dashboard-data")
def dashboard_data():
    # Dynamic Live Data analytics.py එකෙන් ලබා ගැනීම
    if analytics and hasattr(analytics, "get_dashboard_stats"):
        try:
            live_stats = analytics.get_dashboard_stats()
            if live_stats:
                return jsonify(live_stats)
        except Exception as e:
            print(f"❌ Error fetching analytics: {e}")

    # Fallback (analytics නොමැති විට පමණක්)
    fallback_data = {
        "status": "error",
        "totalRounds": "0",
        "averageCrash": "0.00x",
        "highestCrash": "0.00x",
        "lowestCrash": "0.00x",
        "distribution": {
            "below2": "0%",
            "between25": "0%",
            "between510": "0%",
            "above10": "0%"
        },
        "quality": {
            "score": "0%",
            "status": "🔴 No Data"
        }
    }
    return jsonify(fallback_data)

if __name__ == "__main__":
    print("🚀 API Server running on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)