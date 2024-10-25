import os
import json
import requests

# ดึงค่า API_URL และ API_TOKEN จาก Environment Variables
api_url = "https://10.0.15.184/restconf/data/ietf-interfaces:interfaces/interface=Loopback65070193"



# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
basicauth = ("admin", "cisco")


def create():
    yangConfig = {
  "ietf-interfaces:interface": {
    "name": "Loopback65070193",
    "description": "My first RESTCONF loopback",
    "type": "iana-if-type:softwareLoopback",
    "enabled": True,
    "ietf-ip:ipv4": {
      "address": [
        {
          "ip": "172.30.193.1",
          "netmask": "255.255.255.0"
        }
      ]
    }
  }
}

    resp = requests.put(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code == 204):
        print("STATUS OK: {}".format(resp.status_code))
        return "Cannot create: Interface loopback 65070193"
    elif(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070193 is created successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))


def delete():
    resp = requests.delete(
        api_url, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070193 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 65070193"


def enable():
    yangConfig = {"ietf-interfaces:interface":{
    "name": "Loopback65070193",
    "type": "iana-if-type:softwareLoopback",
    "enabled": True,
    
  }}


    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070193 is enabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 65070193"


def disable():
    yangConfig = {"ietf-interfaces:interface": {
    "name": "Loopback65070193",
    "type": "iana-if-type:softwareLoopback",
    "enabled": False,
    }}

    resp = requests.patch(
        api_url, 
        data=json.dumps(yangConfig), 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 65070193 is disabled successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot disable: Interface loopback 65070193"

def status():
    api_url_status = "https://10.0.15.184/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback65070193"

    resp = requests.get(
        api_url_status, 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        print(json.dumps(response_json, indent=4))
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status =  response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 65070193 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 65070193 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 65070193"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
