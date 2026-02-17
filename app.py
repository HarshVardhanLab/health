from flask import Flask, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

HEALTH_API_URL = "https://nova-library-backend.onrender.com/api/v1/health/"

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Keep-alive service is active",
        "target": HEALTH_API_URL
    })

@app.route('/api/ping')
def ping():
    """Endpoint to be called by Vercel Cron"""
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
