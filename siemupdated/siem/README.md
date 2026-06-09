# 🔐 Mini SIEM - Security Information and Event Management

A simple, modular, and professional web-based SIEM system built with Python and Flask. Perfect for learning cybersecurity fundamentals and log analysis.

---

## 📋 Features

✅ **Log Parsing** - Reads and parses structured log files  
✅ **Brute Force Detection** - Alerts on 3+ failed login attempts from same IP  
✅ **DDoS Detection** - Alerts on 5+ requests from same IP  
✅ **Web Dashboard** - Beautiful dark-themed UI with alert management  
✅ **No External Dependencies** - Uses only Flask (plus Werkzeug)  
✅ **Modular Design** - Clean, reusable code structure  

---

## 📁 Project Structure

```
mini_siem/
│
├── app.py                    # Main Flask application
├── logs.txt                  # Sample log file with test data
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── modules/
│   ├── __init__.py          # Package initializer
│   ├── parser.py            # Log parsing module
│   └── detector.py          # Threat detection engine
│
├── templates/
│   └── dashboard.html       # Web dashboard (Jinja2 template)
│
└── static/
    └── style.css            # Dashboard styling
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.7+ installed
- pip package manager

### 2. Installation

```bash
# Navigate to project directory
cd c:\Users\Aryan\Desktop\siem

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

Output:
```
==================================================
🔐 Mini SIEM Starting...
==================================================
📁 Log file: c:\Users\Aryan\Desktop\siem\logs.txt
🌐 Dashboard: http://localhost:5000
==================================================
```

### 4. Access Dashboard

Open your web browser and go to:
```
http://localhost:5000
```

---

## 🎯 How It Works

### Log Format
```
YYYY-MM-DD HH:MM:SS EVENT_TYPE key1=value1 key2=value2
```

**Example:**
```
2026-03-30 10:00:01 LOGIN_FAIL user=admin ip=192.168.1.1
2026-03-30 10:00:02 REQUEST ip=192.168.1.3
```

### Event Types
- `LOGIN_FAIL` - Failed login attempt
- `LOGIN_SUCCESS` - Successful login
- `REQUEST` - HTTP request

### Detection Rules

#### 🔴 Brute Force Detection
- **Trigger:** 3+ LOGIN_FAIL events from same IP
- **Alert:** Displays alert once (no duplicates)
- **Severity:** High

#### 🔴 DDoS Detection
- **Trigger:** 5+ REQUEST events from same IP
- **Alert:** Displays alert once (no duplicates)
- **Severity:** High

---

## 📊 Module Documentation

### `modules/parser.py`
Parses log files and extracts structured data.

**Key Function:**
```python
parse_logs(log_file_path) -> list[dict]
```
Returns list of events with:
- `timestamp` (datetime)
- `event_type` (str)
- `ip` (str)
- `user` (str or None)

### `modules/detector.py`
Detects security threats using rule-based logic.

**Key Class:**
```python
class ThreatDetector:
    def process_events(events) -> list[dict]
```
Returns list of alerts with:
- `type` (str) - Alert type
- `ip` (str) - Source IP
- `severity` (str) - Severity level
- `timestamp` (str) - When alert was triggered

### `app.py`
Flask web application with two routes:
- `GET /` - Renders dashboard with alerts
- `GET /api/alerts` - Returns JSON alerts

---

## 🧪 Test Data

The `logs.txt` file contains sample data that triggers:
- ✅ **Brute Force Alert** - IP 192.168.1.1 has 3 LOGIN_FAIL events
- ✅ **Brute Force Alert** - IP 192.168.1.5 has 3 LOGIN_FAIL events
- ✅ **DDoS Alert** - IP 192.168.1.3 has 5 REQUEST events
- ✅ **DDoS Alert** - IP 10.0.0.1 has 5 REQUEST events

Result: **4 total alerts** displayed on dashboard

---

## 🎨 Dashboard Features

- **Dark Theme** - Eye-friendly cybersecurity aesthetic
- **Alert Counter** - Total alerts at a glance
- **Status Indicator** - System secure or threats detected
- **Alert Table** - Detailed view of all alerts
- **Auto-Refresh** - Dashboard refreshes every 30 seconds
- **Responsive Design** - Works on desktop, tablet, mobile

---

## 📝 Sample Log File Format

```
2026-03-30 10:00:01 LOGIN_FAIL user=admin ip=192.168.1.1
2026-03-30 10:00:02 LOGIN_SUCCESS user=john ip=192.168.1.2
2026-03-30 10:00:03 REQUEST ip=192.168.1.3
2026-03-30 10:00:04 LOGIN_FAIL user=admin ip=192.168.1.1
2026-03-30 10:00:05 REQUEST ip=192.168.1.3
2026-03-30 10:00:06 LOGIN_FAIL user=admin ip=192.168.1.1
```

---

## 🔧 Customization

### Add Custom Detection Rules

Edit `modules/detector.py` and add logic to `process_events()`:

```python
# Example: Alert on specific username
if event['user'] == 'admin' and event_type == 'LOGIN_FAIL':
    self._create_alert(...)
```

### Modify Alert Thresholds

In `modules/detector.py`:
```python
# Change brute force threshold from 3 to 5
if self.login_fail_count[ip] >= 5 and ip not in self.brute_force_ips:

# Change DDoS threshold from 5 to 10
if self.request_count[ip] >= 10 and ip not in self.ddos_ips:
```

### Custom Log Format

Modify parsing logic in `modules/parser.py` to support different log formats.

---

## 🐛 Troubleshooting

**Issue:** Flask not found
```bash
pip install -r requirements.txt
```

**Issue:** Port 5000 already in use
```bash
# Run on different port
# Edit app.py: app.run(port=5001)
```

**Issue:** logs.txt not found
```
Ensure logs.txt exists in the same directory as app.py
```

**Issue:** No alerts showing
```
1. Check logs.txt file exists
2. Verify log format matches specification
3. Check browser console for errors
4. Refresh page (F5)
```

---

## 📚 Learning Points

This project demonstrates:
- ✅ Flask web framework fundamentals
- ✅ Modular code organization
- ✅ File I/O and parsing in Python
- ✅ Rule-based threat detection
- ✅ Web UI design (HTML + CSS)
- ✅ Jinja2 templating
- ✅ Security event processing

---

## 💡 Future Enhancements

- Add database support (SQLite/PostgreSQL)
- Implement time-based detection windows
- Add email/SMS alert notifications
- Create custom rules UI
- Add log filtering/search
- Implement role-based access control
- Add real-time WebSocket updates
- Create export functionality (PDF/CSV)

---

## 📄 License

Free to use for educational purposes.

---

## 👨‍💻 Author

Built with ❤️ for cybersecurity enthusiasts and learners.

**Version:** 1.0  
**Created:** 2026-03-30  
**Python Version:** 3.7+

---

## 📞 Support

For issues or questions, review the code comments and docstrings. All functions are well-documented.

Happy learning! 🚀🔐
