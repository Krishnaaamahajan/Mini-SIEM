"""
Mini SIEM Web Application
Flask-based Security Information and Event Management system
"""

import os
import json
from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from modules.parser import parse_logs
from modules.detector import ThreatDetector
from modules.scp_loader import fetch_logs_via_scp


# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'super_secret_siem_key'  # Needed for flash messages

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, 'logs.txt')
CONFIG_FILE_PATH = os.path.join(BASE_DIR, 'config.json')


def load_config():
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config):
    with open(CONFIG_FILE_PATH, 'w') as f:
        json.dump(config, f)


@app.route('/')
def dashboard():
    """
    Main dashboard route.
    Parses logs, detects threats, and renders the dashboard.
    """
    # Load config
    config = load_config()
    
    # Parse logs from file
    events = parse_logs(LOG_FILE_PATH)
    
    # Detect threats
    detector = ThreatDetector()
    alerts = detector.process_events(events)
    
    # Render dashboard template with alerts and config
    return render_template('dashboard.html', alerts=alerts, alert_count=len(alerts), config=config)

@app.route('/api/fetch_logs', methods=['POST'])
def fetch_logs():
    """
    Endpoint to fetch logs via SCP.
    """
    host = request.form.get('host')
    port = int(request.form.get('port', 22))
    username = request.form.get('username')
    password = request.form.get('password')
    remote_path = request.form.get('remote_path')
    
    # Save config (excluding password)
    config = {
        'host': host,
        'port': port,
        'username': username,
        'remote_path': remote_path
    }
    save_config(config)
    
    # Attempt SCP fetch
    success, message = fetch_logs_via_scp(
        host=host,
        port=port,
        user=username,
        password=password,
        remote_path=remote_path,
        local_path=LOG_FILE_PATH
    )
    
    if success:
        flash(message, 'success')
    else:
        flash(message, 'error')
        
    return redirect(url_for('dashboard'))


@app.route('/api/alerts')
def get_alerts():
    """
    API endpoint to get alerts as JSON.
    """
    # Parse logs from file
    events = parse_logs(LOG_FILE_PATH)
    
    # Detect threats
    detector = ThreatDetector()
    alerts = detector.process_events(events)
    
    return jsonify({
        'alert_count': len(alerts),
        'alerts': alerts
    })


if __name__ == '__main__':
    print("=" * 50)
    print("🔐 Mini SIEM Starting...")
    print("=" * 50)
    print(f"📁 Log file: {LOG_FILE_PATH}")
    print(f"🌐 Dashboard: http://localhost:5000")
    print("=" * 50)
    
    # Run the Flask application
    app.run(debug=True, host='localhost', port=5000)
