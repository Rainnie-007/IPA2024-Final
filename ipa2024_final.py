#######################################################################################
# Yourname:Yongyut Chanuphat
# Your student ID: 65070193
# Your GitHub Repo: https://github.com/Rainnie-007/IPA2024-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import requests
import json 
import time
import os
import restconf_final as restconf
import netmiko_final as netmiko
import ansible_final as ansible
from requests_toolbelt.multipart.encoder import MultipartEncoder

#######################################################################################
# 2. Assign the Webex access token to the variable accessToken using environment variables.

accessToken = os.getenv('API_TOKEN')
# accessToken = "Bearer MGJiM2U4ZDQtNjFjMS00N2M0LWIxMGUtN2ZhNzRmYzllMWJkMWI4ZmE1NDEtNDFk_P0A1_1ad92174-dfe2-4740-b008-57218895946c"
if accessToken is not None:
    accessToken = f"Bearer {accessToken}"
else:
    raise Exception("API token is not set in the environment variables.")
#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vMjQyNzJiMTAtNTVhYi0xMWVmLThkYWMtY2RiYzIzYWFmMWJj"
)

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}
    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {
    "Authorization": accessToken
}


# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/65070193"):

        # extract the command
        command = message.split(" ", 1)
        final = command[1]
        print(final)

# 5. Complete the logic for each command

        if final == "create":
            responseMessage = restconf.create()    
        elif final == "delete":
            responseMessage = restconf.delete()
        elif final == "enable":
            responseMessage = restconf.enable()
        elif final == "disable":
            responseMessage = restconf.disable()
        elif final == "status":
            responseMessage = restconf.status()
        elif final == "gigabit_status":
            responseMessage = netmiko.gigabit_status()
        elif final == "showrun":
            student_id = '65070193'  # Replace with your student ID
            router_name = 'IPA2024-Pod1-4'  # Replace with your router name
            responseMessage = ansible.showrun(student_id, router_name)

        else:
            responseMessage = "Error: No command or unknown command"
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            filename = "show_running_config.txt"
            fileobject = open(filename, 'rb')  # เปิดไฟล์สำหรับการแนบ
            filetype = "text/plain"
            postData = {
                "roomId": roomIdToGetMessages,  # กำหนด roomId จากตัวแปรที่ประกาศไว้ข้างบน
                "text": "show running config",  # ข้อความที่ต้องการส่ง
                "files": (filename, fileobject, filetype),  # ใส่ข้อมูลไฟล์แนบ
            }
            postData = MultipartEncoder(postData)
            HTTPHeaders = {
                "Authorization": accessToken,
                "Content-Type": postData.content_type  # กำหนด Content-Type จาก postData
            }
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId": roomIdToGetMessages, "text": responseMessage}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {"Authorization": accessToken, "Content-Type": "application/json"}   

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data= postData,
            headers= HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
