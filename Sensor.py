import paramiko
import os
import difflib
import sys

# Configuration
switch_ip = "192.168.1.1"  # Replace with your switch's IP address
username = "admin"         # Replace with your SSH username
password = "password"      # Replace with your SSH password
config_file_path = "/path/to/current-switch-config.txt"  # Path to save the fetched configuration
baseline_file_path = "/path/to/baseline-switch-config.txt" # Path to the baseline configuration file

def fetch_configuration():
    """Fetch the running configuration from the Cisco switch via SSH."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(switch_ip, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command('show running-config')
        config = stdout.read().decode()
        
        with open(config_file_path, 'w') as f:
            f.write(config)
        
        print("Configuration fetched and saved to", config_file_path)
    
    except Exception as e:
        print(f"Error fetching configuration: {e}")
    
    finally:
        ssh.close()

def compare_configurations():
    """Compare the fetched configuration with the baseline configuration."""
    if not os.path.exists(config_file_path):
        print(f"Configuration file {config_file_path} does not exist.")
        return
    
    with open(config_file_path, 'r') as f:
        current_config = f.readlines()
    
    with open(baseline_file_path, 'r') as f:
        baseline_config = f.readlines()
    
    diff = list(difflib.unified_diff(baseline_config, current_config, lineterm=''))
    
    if diff:
        print("Configuration drift detected:")
        for line in diff:
            print(line, end='')
    else:
        print("Configuration is in sync.")

if __name__ == "__main__":
    fetch_configuration()
    compare_configurations()
