from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.181"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}

def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        interface_statuses = []  
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        
        for status in result:
            if "GigabitEthernet" in status['interface']:  
                interface_name = status['interface']
                interface_status = status['status']  
                
                # Store each interface status
                interface_statuses.append(f"{interface_name} {interface_status}")

                if interface_status == "up":
                    up += 1
                elif interface_status == "down":
                    down += 1
                elif interface_status == "administratively down":
                    admin_down += 1
        
        
        detailed_status = ", ".join(interface_statuses)
        
        
        ans = f"{detailed_status} -> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans


