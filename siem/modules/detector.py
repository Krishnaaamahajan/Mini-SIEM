"""
Threat Detection Module
Detects security threats based on log events.
"""

from datetime import datetime


class ThreatDetector:
    """
    Detects security threats using rule-based logic.
    """
    
    def __init__(self):
        """Initialize the threat detector with empty counters."""
        self.alerts = []
        self.brute_force_ips = set()  # Track IPs already alerted for brute force
        self.ddos_ips = set()         # Track IPs already alerted for DDoS
        self.login_fail_count = {}    # Count of failed logins per IP
        self.request_count = {}       # Count of requests per IP
    
    def process_events(self, events):
        """
        Process events and detect threats.
        
        Args:
            events (list): List of parsed log events
            
        Returns:
            list: List of generated alerts
        """
        # Reset counters for fresh detection
        self.login_fail_count = {}
        self.request_count = {}
        self.alerts = []
        self.brute_force_ips = set()
        self.ddos_ips = set()
        
        # Process each event
        for event in events:
            event_type = event['event_type']
            ip = event['ip']
            timestamp = event['timestamp']
            
            # Handle LOGIN_FAIL events
            if event_type == 'LOGIN_FAIL':
                self.login_fail_count[ip] = self.login_fail_count.get(ip, 0) + 1
                
                # Check if threshold reached for brute force detection
                if self.login_fail_count[ip] >= 3 and ip not in self.brute_force_ips:
                    self._create_alert(
                        alert_type='Brute Force',
                        ip=ip,
                        severity='High',
                        timestamp=timestamp
                    )
                    self.brute_force_ips.add(ip)
            
            # Handle REQUEST events
            elif event_type == 'REQUEST':
                self.request_count[ip] = self.request_count.get(ip, 0) + 1
                
                # Check if threshold reached for DDoS detection
                if self.request_count[ip] >= 5 and ip not in self.ddos_ips:
                    self._create_alert(
                        alert_type='DDoS',
                        ip=ip,
                        severity='High',
                        timestamp=timestamp
                    )
                    self.ddos_ips.add(ip)
        
        return self.alerts
    
    def _create_alert(self, alert_type, ip, severity, timestamp):
        """
        Create and store an alert.
        
        Args:
            alert_type (str): Type of alert (Brute Force, DDoS)
            ip (str): IP address of the threat source
            severity (str): Severity level (High)
            timestamp (datetime): When the alert was triggered
        """
        alert = {
            'type': alert_type,
            'ip': ip,
            'severity': severity,
            'timestamp': timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.alerts.append(alert)
    
    def get_alerts(self):
        """
        Get all detected alerts.
        
        Returns:
            list: List of alerts
        """
        return self.alerts
