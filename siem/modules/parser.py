"""
Log Parser Module
Parses log files and extracts structured event data.
"""

from datetime import datetime


import re

def parse_logs(log_file_path):
    """
    Parse logs from a file and extract structured data.
    Supports both the custom Mini SIEM format and standard Linux auth.log formats.
    """
    events = []
    
    # Regex for standard Linux auth.log SSH login attempts
    # Example: May  4 10:20:30 hostname sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
    auth_failed_re = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+)")
    auth_accepted_re = re.compile(r"Accepted password for (?P<user>\S+) from (?P<ip>\S+)")
    
    # Regex for custom Mini SIEM format
    # Example: 2026-05-04 10:20:30 LOGIN_FAIL ip=192.168.1.100 user=admin
    custom_format_re = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<event_type>\S+)\s+(?P<remaining>.*)$")
    
    # Basic syslog timestamp regex (e.g. "May  4 10:20:30")
    syslog_time_re = re.compile(r"^(?P<month>[A-Z][a-z]{2})\s+(?P<day>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2})")

    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                event_data = {
                    'timestamp': datetime.now(), # Default to now if parsing fails
                    'event_type': None,
                    'ip': None,
                    'user': None
                }

                # Try custom format first
                custom_match = custom_format_re.match(line)
                if custom_match:
                    try:
                        date_str = custom_match.group('date')
                        time_str = custom_match.group('time')
                        event_data['timestamp'] = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
                        event_data['event_type'] = custom_match.group('event_type')
                        
                        remaining = custom_match.group('remaining')
                        for pair in remaining.split():
                            if '=' in pair:
                                key, value = pair.split('=', 1)
                                if key == 'ip':
                                    event_data['ip'] = value
                                elif key == 'user':
                                    event_data['user'] = value
                    except ValueError:
                        pass
                
                # If not custom, try standard Linux auth.log format
                else:
                    # Try to parse syslog timestamp
                    syslog_match = syslog_time_re.match(line)
                    if syslog_match:
                        try:
                            # Syslog doesn't include year, so we assume current year
                            current_year = datetime.now().year
                            month_str = syslog_match.group('month')
                            day_str = syslog_match.group('day')
                            time_str = syslog_match.group('time')
                            # Handle month abbreviation mapping
                            timestamp = datetime.strptime(f"{current_year} {month_str} {day_str} {time_str}", "%Y %b %d %H:%M:%S")
                            # If date is in the future, it might be from last year
                            if timestamp > datetime.now():
                                timestamp = timestamp.replace(year=current_year - 1)
                            event_data['timestamp'] = timestamp
                        except ValueError:
                            pass
                            
                    # Check for SSH Failed Login
                    failed_match = auth_failed_re.search(line)
                    if failed_match:
                        event_data['event_type'] = 'LOGIN_FAIL'
                        event_data['user'] = failed_match.group('user')
                        event_data['ip'] = failed_match.group('ip')
                    else:
                        # Check for SSH Accepted Login
                        accepted_match = auth_accepted_re.search(line)
                        if accepted_match:
                            event_data['event_type'] = 'LOGIN_SUCCESS'
                            event_data['user'] = accepted_match.group('user')
                            event_data['ip'] = accepted_match.group('ip')
                
                # Only add if we have an IP and an event type
                if event_data['ip'] and event_data['event_type']:
                    events.append(event_data)
    
    except FileNotFoundError:
        print(f"Error: Log file '{log_file_path}' not found.")
        return []
    
    return events
