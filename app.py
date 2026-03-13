from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
from threading import Thread
import time
import os

app = Flask(__name__)

# URLs to monitor
URLS = {
    "nova": {
        "url": "https://nova-library-backend.onrender.com/api/v1/health/",
        "label": "Nova Library Backend",
        "status": "Checking...",
        "code": "",
        "last_checked": ""
    },
    "excel": {
        "url": "https://excel-153y.onrender.com",
        "label": "Excel Service",
        "status": "Checking...",
        "code": "",
        "last_checked": ""
    }
}


def check_url(key):
    """Check a single URL and update its status data."""
    target = URLS[key]
    try:
        response = requests.get(target["url"], timeout=10)
        target["status"] = "Online ✅"
        target["code"] = str(response.status_code)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{target['label']}] Status: {response.status_code}")
    except Exception as e:
        target["status"] = "Offline ❌"
        target["code"] = "Error"
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{target['label']}] Error: {str(e)}")
    target["last_checked"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def ping_all_endpoints():
    """Continuously ping all health endpoints every 30 seconds."""
    while True:
        for key in URLS:
            check_url(key)
        time.sleep(30)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/status')
def status():
    """Return current status of all monitored URLs."""
    result = {}
    for key, data in URLS.items():
        result[key] = {
            "label": data["label"],
            "url": data["url"],
            "status": data["status"],
            "code": data["code"],
            "last_checked": data["last_checked"]
        }
    return jsonify(result)


@app.route('/api/ping')
def ping():
    """Manually trigger a ping of all URLs."""
    for key in URLS:
        check_url(key)
    return jsonify({
        "success": True,
        "timestamp": datetime.now().isoformat(),
        "results": {k: {"status": v["status"], "code": v["code"]} for k, v in URLS.items()}
    })


if __name__ == '__main__':
    # Start the background thread for pinging
    ping_thread = Thread(target=ping_all_endpoints, daemon=True)
    ping_thread.start()

    # Get port from environment variable
    port = int(os.environ.get('PORT', 5000))

    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
