# 🚀 QUICK START GUIDE - Mini SIEM

## Installation & Setup (5 minutes)

### Step 1: Install Dependencies
```bash
cd c:\Users\Aryan\Desktop\siem
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Open Dashboard
Go to: **http://localhost:5000**

---

## ✅ Expected Results

When you open the dashboard, you should see:

**Header:** 🔐 Mini SIEM Dashboard

**Stats:**
- Total Alerts: **4**
- Status: ⚠️ THREATS DETECTED

**Alerts Table (4 rows):**
```
┌─────────────────┬─────────────────┬───────────┬──────────────────────┐
│ Alert Type      │ IP Address      │ Severity  │ Timestamp            │
├─────────────────┼─────────────────┼───────────┼──────────────────────┤
│ 🔴 Brute Force  │ 192.168.1.1     │ High      │ 2026-03-30 10:00:06  │
│ 🔴 DDoS         │ 192.168.1.3     │ High      │ 2026-03-30 10:00:10  │
│ 🔴 DDoS         │ 10.0.0.1        │ High      │ 2026-03-30 10:00:17  │
│ 🔴 Brute Force  │ 192.168.1.5     │ High      │ 2026-03-30 10:00:19  │
└─────────────────┴─────────────────┴───────────┴──────────────────────┘
```

---

## 🎯 How Detection Works

### Brute Force (3 failed logins from same IP)
```
IP: 192.168.1.1
- 10:00:01 LOGIN_FAIL ✗
- 10:00:04 LOGIN_FAIL ✗
- 10:00:06 LOGIN_FAIL ✗ → ALERT!
```

### DDoS (5 requests from same IP)
```
IP: 192.168.1.3
- 10:00:03 REQUEST ✓
- 10:00:05 REQUEST ✓
- 10:00:07 REQUEST ✓
- 10:00:08 REQUEST ✓
- 10:00:10 REQUEST ✓ → ALERT!
```

---

## 🧪 Testing Custom Logs

### Edit logs.txt
Add these lines to test:
```
2026-03-30 10:05:01 LOGIN_FAIL user=hacker ip=203.0.113.1
2026-03-30 10:05:02 LOGIN_FAIL user=hacker ip=203.0.113.1
2026-03-30 10:05:03 LOGIN_FAIL user=hacker ip=203.0.113.1
```

### Refresh Dashboard
Press F5 or wait 30 seconds for auto-refresh.

### Expected Result
New alert for IP: 203.0.113.1 (Brute Force)

---

## 📱 API Usage

### Get Alerts as JSON
```bash
curl http://localhost:5000/api/alerts
```

**Response:**
```json
{
  "alert_count": 4,
  "alerts": [
    {
      "type": "Brute Force",
      "ip": "192.168.1.1",
      "severity": "High",
      "timestamp": "2026-03-30 10:00:06"
    },
    ...
  ]
}
```

---

## 🛑 Stop the Application

Press **Ctrl+C** in the terminal.

---

## 💻 File Overview

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application (125 lines) |
| `modules/parser.py` | Log parsing logic (75 lines) |
| `modules/detector.py` | Threat detection (95 lines) |
| `templates/dashboard.html` | Web dashboard (125 lines) |
| `static/style.css` | Styling (300+ lines) |
| `logs.txt` | Sample log data (20 events) |

---

## ✨ Code Quality

✅ Clean, modular code  
✅ Comprehensive docstrings  
✅ Error handling  
✅ No external dependencies (except Flask)  
✅ PEP 8 style compliance  
✅ Production-ready code structure  

---

## 🎓 Learning Outcomes

After running this project, you'll understand:
1. How SIEM systems work
2. Log parsing and processing
3. Rule-based threat detection
4. Flask web development
5. HTML/CSS dashboard design
6. Security event correlation

---

## 🐍 Python Concepts Used

- File I/O (`open()`, `read()`)
- String parsing and splitting
- Datetime handling
- Dictionaries and sets
- Object-oriented programming (OOP)
- List comprehensions
- Exception handling
- Flask decorators
- Jinja2 templating

---

## 🔐 Security Notes

This is an **educational project** for learning purposes:
- ✅ Safe for local testing
- ✅ No network exposure required
- ✅ No sensitive data logging
- ⚠️ Not for production use
- ⚠️ Add authentication before production deployment

---

## 📞 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.7+ |
| Flask error | Run: `pip install -r requirements.txt` |
| Port 5000 in use | Change port in `app.py` line 42 |
| No alerts showing | Verify `logs.txt` in correct directory |
| Dashboard blank | Clear browser cache, refresh page |

---

**Enjoy your SIEM journey! 🚀🔐**
