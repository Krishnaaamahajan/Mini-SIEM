"""
SCP Loader Module
Downloads remote log files securely using SSH/SCP.
"""

import paramiko
import os

def fetch_logs_via_scp(host, port, user, password, remote_path, local_path):
    """
    Downloads a file from a remote server using SCP/SFTP.
    
    Args:
        host (str): Remote server hostname or IP
        port (int): SSH port (usually 22)
        user (str): SSH username
        password (str): SSH password
        remote_path (str): Path to the log file on the remote server
        local_path (str): Where to save the downloaded log file locally
        
    Returns:
        bool: True if successful, False otherwise
        str: Message indicating success or error details
    """
    ssh = paramiko.SSHClient()
    # Automatically add host keys for first-time connections
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Connect to the remote server
        ssh.connect(hostname=host, port=port, username=user, password=password, timeout=10)
        
        # Use SFTP to download the file
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
        
        return True, f"Successfully downloaded logs from {host}:{remote_path}"
    
    except paramiko.AuthenticationException:
        return False, "Authentication failed. Please check your username and password."
    except paramiko.SSHException as e:
        return False, f"SSH connection failed: {str(e)}"
    except FileNotFoundError:
        return False, f"Remote file not found: {remote_path}"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"
    finally:
        ssh.close()
