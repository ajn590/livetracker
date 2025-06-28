from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)
os.makedirs("snapshots", exist_ok=True)

@app.route("/")
def home():
    return "✅ Flask Tracker is Running"

@app.route("/location", methods=["POST"])
def location():
    data = request.get_json()
    print("📍 Location Received:", data)
    with open("location_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {data}\n")
    return "Location received"

@app.route("/upload", methods=["POST"])
def upload():
    img = request.files["snapshot"]
    filename = f"snapshots/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    img.save(filename)
    print(f"📸 Snapshot saved: {filename}")
    return "Snapshot received"
