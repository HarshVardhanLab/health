from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
from threading import Thread
import time
import os

app = Flask(__name__)

HEALTH_API_URL = "https://nova-library-backend.onrender.com/api/v1/health/"

def ping_health_endpoint():
    """Continuously ping the health endpoint every 30 seconds"""
    while True:
        try:
            response = requests.get(HEALTH_API_URL, timeout=10)
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Health check: {response.status_code}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error: {str(e)}")
        
        time.sleep(30)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/ping')
def ping():
    """Manual ping endpoint"""
    try:
        response = requests.get(HEALTH_API_URL, timeout=10)
        return jsonify({
            "success": True,
            "status_code": response.status_code,
            "timestamp": datetime.now().isoformat(),
            "target": HEALTH_API_URL
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
            "target": HEALTH_API_URL
        }), 500

if __name__ == '__main__':
    # Start the background thread for pinging
    ping_thread = Thread(target=ping_health_endpoint, daemon=True)
    ping_thread.start()
    
    # Get port from environment variable (Railway provides this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
