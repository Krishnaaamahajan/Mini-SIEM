# 🧪 Testing & Advanced Usage Guide

## Interactive Testing Guide

This guide shows you how to test the Mini SIEM system with different scenarios.

---

## Test 1: View Current Alerts

### What to Do
1. Open browser: `http://localhost:5000`
2. Observe the dashboard

### Expected Results
```
✅ Total Alerts: 4
✅ Status: ⚠️ THREATS DETECTED
✅ Alert Table shows:
   - Brute Force: 192.168.1.1
   - DDoS: 192.168.1.3
   - DDoS: 10.0.0.1
   - Brute Force: 192.168.1.5
```

---

## Test 2: Get JSON Data (API)

### What to Do
```bash
# In PowerShell or Terminal
curl http://localhost:5000/api/alerts
```

### Expected Results
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

## Test 3: Add New Brute Force Event

### What to Do
1. **Edit logs.txt** - Add these lines at the end:
```
2026-03-30 10:15:01 LOGIN_FAIL user=hacker ip=203.0.113.1
2026-03-30 10:15:02 LOGIN_FAIL user=hacker ip=203.0.113.1
2026-03-30 10:15:03 LOGIN_FAIL user=hacker ip=203.0.113.1
```

2. **Refresh dashboard** - F5 or wait 30 seconds

### Expected Results
```
✅ Total Alerts: 5 (increased from 4)
✅ New alert row added:
   - Type: Brute Force
   - IP: 203.0.113.1
   - Severity: High
   - Timestamp: 2026-03-30 10:15:03
```

---

## Test 4: Add New DDoS Event

### What to Do
1. **Edit logs.txt** - Add these lines at the end:
```
2026-03-30 10:20:01 REQUEST ip=198.51.100.1
2026-03-30 10:20:02 REQUEST ip=198.51.100.1
2026-03-30 10:20:03 REQUEST ip=198.51.100.1
2026-03-30 10:20:04 REQUEST ip=198.51.100.1
2026-03-30 10:20:05 REQUEST ip=198.51.100.1
```

2. **Refresh dashboard**

### Expected Results
```
✅ Total Alerts: 6 (increased from 5)
✅ New alert row added:
   - Type: DDoS
   - IP: 198.51.100.1
   - Severity: High
   - Timestamp: 2026-03-30 10:20:05
```

---

## Test 5: Verify No Duplicate Alerts

### What to Do
1. **Edit logs.txt** - Add these lines (same IP as first test):
```
2026-03-30 10:25:01 LOGIN_FAIL user=admin ip=192.168.1.1
2026-03-30 10:25:02 LOGIN_FAIL user=admin ip=192.168.1.1
```

2. **Refresh dashboard**

### Expected Results
```
✅ Total Alerts: 6 (UNCHANGED)
✅ NO new alert for 192.168.1.1
✅ Reason: Already alerted for this IP
```

**This demonstrates the duplicate prevention logic!**

---

## Test 6: Verify Alert Only at Threshold

### What to Do
1. **Edit logs.txt** - Add these lines:
```
2026-03-30 10:30:01 LOGIN_FAIL user=newuser ip=198.51.101.1
2026-03-30 10:30:02 LOGIN_FAIL user=newuser ip=198.51.101.1
```

2. **Refresh dashboard**

### Expected Results
```
✅ Total Alerts: 6 (UNCHANGED)
✅ NO new alert for 198.51.101.1
✅ Reason: Only 2 failures (threshold is 3)
```

3. **Add one more failure:**
```
2026-03-30 10:30:03 LOGIN_FAIL user=newuser ip=198.51.101.1
```

4. **Refresh dashboard**

### Expected Results
```
✅ Total Alerts: 7 (increased)
✅ New alert for 198.51.101.1 appears
✅ Reason: Reached threshold of 3
```

---

## Test 7: Mixed Events (Success + Failure)

### What to Do
1. **Edit logs.txt** - Add these lines:
```
2026-03-30 10:35:01 LOGIN_FAIL user=bob ip=198.51.102.1
2026-03-30 10:35:02 LOGIN_SUCCESS user=bob ip=198.51.102.1
2026-03-30 10:35:03 LOGIN_FAIL user=bob ip=198.51.102.1
2026-03-30 10:35:04 LOGIN_SUCCESS user=bob ip=198.51.102.1
2026-03-30 10:35:05 LOGIN_FAIL user=bob ip=198.51.102.1
```

2. **Refresh dashboard**

### Expected Results
```
✅ Total Alerts: 8 (increased)
✅ New alert for 198.51.102.1 appears
✅ SUCCESS events are ignored
✅ Only 3 FAIL events count
```

---

## Test 8: Monitor Real-Time Auto-Refresh

### What to Do
1. **Open two tabs:**
   - Tab 1: `http://localhost:5000`
   - Tab 2: Code editor with logs.txt

2. **Add events to logs.txt in Tab 2**
3. **Observe Tab 1 auto-refresh every 30 seconds**

### Expected Results
```
✅ Dashboard auto-refreshes every 30 seconds
✅ New alerts appear automatically
✅ Timestamp updates in footer
✅ No manual refresh needed
```

---

## Test 9: Test Responsiveness

### What to Do
1. **Open dashboard**
2. **Resize browser window:**
   - Small (mobile)
   - Medium (tablet)
   - Large (desktop)

### Expected Results
```
✅ Mobile view (< 480px)
   - Single column layout
   - Readable text
   - Scrollable table

✅ Tablet view (480px - 768px)
   - Two column stats
   - Compact table
   - Touch-friendly

✅ Desktop view (> 768px)
   - Full layout
   - Side-by-side stats
   - Expanded table
```

---

## Test 10: Edge Cases

### Empty File Test
1. **Create empty logs.txt**
2. **Refresh dashboard**

### Expected Results
```
✅ Total Alerts: 0
✅ Status: ✅ SYSTEM SECURE
✅ Message: "No security threats detected"
```

### Malformed Log Test
1. **Add invalid log line:**
```
This is not a valid log format
2026-03-30 INVALID_FORMAT
192.168.1.1 without timestamp
```

2. **Refresh dashboard**

### Expected Results
```
✅ Dashboard still loads
✅ Invalid lines are skipped
✅ Valid alerts still show
✅ No errors in console
```

---

## Performance Tests

### Test Large Log File
1. **Generate 100+ events:**
```bash
# Quick way to add many events
for i in {1..10}; do echo "2026-03-30 10:45:0$i REQUEST ip=172.16.1.$i" >> logs.txt; done
```

2. **Refresh dashboard**

### Expected Results
```
✅ Dashboard loads instantly
✅ No lag or slowdown
✅ All alerts detected correctly
✅ Performance remains fast
```

---

## Debugging

### View Parser Output
1. **Edit app.py** - Add debug logging:
```python
@app.route('/')
def dashboard():
    events = parse_logs(LOG_FILE_PATH)
    print(f"Parsed events: {len(events)}")
    for event in events[:5]:
        print(event)
    ...
```

2. **Restart app and check terminal output**

### View Detector Output
1. **Edit detector.py** - Add debug output:
```python
def process_events(self, events):
    ...
    print(f"Login fail count: {self.login_fail_count}")
    print(f"Request count: {self.request_count}")
    ...
```

### Browser Console
1. **Press F12** to open developer tools
2. **Go to Console tab**
3. **Check for JavaScript errors**

---

## Sample Test Scenarios

### Scenario 1: Red Team Attack
```
# Brute force attack on admin account
2026-03-30 11:00:01 LOGIN_FAIL user=admin ip=203.0.113.50
2026-03-30 11:00:02 LOGIN_FAIL user=admin ip=203.0.113.50
2026-03-30 11:00:03 LOGIN_FAIL user=admin ip=203.0.113.50
2026-03-30 11:00:04 LOGIN_FAIL user=admin ip=203.0.113.50
2026-03-30 11:00:05 LOGIN_FAIL user=admin ip=203.0.113.50

# DDoS attack
2026-03-30 11:00:10 REQUEST ip=203.0.113.100
2026-03-30 11:00:11 REQUEST ip=203.0.113.100
2026-03-30 11:00:12 REQUEST ip=203.0.113.100
2026-03-30 11:00:13 REQUEST ip=203.0.113.100
2026-03-30 11:00:14 REQUEST ip=203.0.113.100
2026-03-30 11:00:15 REQUEST ip=203.0.113.100
2026-03-30 11:00:16 REQUEST ip=203.0.113.100
```

### Scenario 2: Normal Operations
```
# Legitimate user activity
2026-03-30 11:30:01 LOGIN_SUCCESS user=john ip=192.168.1.50
2026-03-30 11:30:05 REQUEST ip=192.168.1.50
2026-03-30 11:30:10 REQUEST ip=192.168.1.50
2026-03-30 11:30:15 REQUEST ip=192.168.1.50
2026-03-30 11:30:20 REQUEST ip=192.168.1.50
```

### Scenario 3: Multiple Attackers
```
# Attacker 1
2026-03-30 11:45:01 REQUEST ip=198.51.100.1
2026-03-30 11:45:02 REQUEST ip=198.51.100.1
2026-03-30 11:45:03 REQUEST ip=198.51.100.1
2026-03-30 11:45:04 REQUEST ip=198.51.100.1
2026-03-30 11:45:05 REQUEST ip=198.51.100.1

# Attacker 2
2026-03-30 11:45:10 LOGIN_FAIL user=guest ip=198.51.101.1
2026-03-30 11:45:11 LOGIN_FAIL user=guest ip=198.51.101.1
2026-03-30 11:45:12 LOGIN_FAIL user=guest ip=198.51.101.1
```

---

## Troubleshooting Tests

### If Alerts Don't Appear
1. **Check logs.txt exists** in correct directory
2. **Verify log format:**
   - Must have: `YYYY-MM-DD HH:MM:SS EVENT_TYPE key=value`
   - Example: `2026-03-30 10:00:01 LOGIN_FAIL user=admin ip=192.168.1.1`
3. **Check browser console** (F12) for errors
4. **Check terminal** where app.py is running for errors
5. **Force refresh** dashboard (Ctrl+Shift+R)

### If Dashboard Won't Load
1. **Check Flask is running** - Look for "Running on http://localhost:5000"
2. **Check port 5000** isn't blocked
3. **Try different port** - Edit app.py line 42
4. **Check Python errors** in terminal
5. **Restart application** - Ctrl+C and python app.py

### If Styling Looks Wrong
1. **Clear browser cache** - Ctrl+Shift+Delete
2. **Force refresh** - Ctrl+F5
3. **Check style.css** file exists in /static
4. **Check browser console** for CSS errors

---

## ✅ Test Checklist

- [ ] View current dashboard
- [ ] Test API endpoint
- [ ] Add brute force event
- [ ] Add DDoS event
- [ ] Verify no duplicates
- [ ] Test threshold logic
- [ ] Mix success/fail events
- [ ] Auto-refresh works
- [ ] Responsive design
- [ ] Edge cases handled
- [ ] Performance good
- [ ] No console errors

---

**Happy Testing! 🚀🔐**
