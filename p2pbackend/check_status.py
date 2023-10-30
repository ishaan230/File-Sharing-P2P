import subprocess
import platform

def check_host_online(ip_address):
    operating_system = platform.system().lower()

    if operating_system == "windows":
        command = ['ping', '-n', '1', ip_address]
    else:
        command = ['ping', '-c', '1', ip_address]
    try:
        result = subprocess.run(command, timeout=5, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #it returns true if result.returncode is 0
        if result.returncode == 0:
            return 'online'
        else:
            return 'offline'
    except subprocess.TimeoutExpired:
        return False

ip_to_check = '8.8.8.8'
print(check_host_online(ip_to_check))
