"""
Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI
import os
import json

# get environment variables
#WT_BOT_TOKEN = os.environ['WT_BOT_TOKEN']
WT_BOT_TOKEN = 'OTcyMzcwMTYtNmQwNC00ODk0LWIzMGQtMTMxNzNhNmQ0NmY5OTQ4ZDIyZTMtNzE4_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f'

# uncomment next line if you are implementing a notifier bot
#WT_ROOM_ID = os.environ['WT_ROOM_ID']
WT_ROOM_ID = 'Y2lzY29zcGFyazovL3VzL1JPT00vOGQ4ZmU3NjAtZDViNC0xMWViLTg3OTItZWQ5ZDVkMDdlY2Iw'

# uncomment next line if you are implementing a controller bot
#WT_BOT_EMAIL = os.environ['WT_BOT_EMAIL']

# start Flask and WT connection
app = Flask(__name__)
api = WebexTeamsAPI(access_token=WT_BOT_TOKEN)


# defining the decorater and route registration for incoming alerts
@app.route('/', methods=['POST'])
def alert_received():
    raw_json = request.get_json()
    print(raw_json)

    # customize the behaviour of the bot here
#    message = "Hi, I am a Webex Teams bot. Have a great day ☀! "
#    message = raw_json['version']
    if 'dnacIP' in raw_json :
        message = '<@all>\r\n';
        message += raw_json['dnacIP'] + 'からアラートが通知されています \r\n';
        message += 'イベントID:' + raw_json['eventId'] + '\r\n';
        message += 'シビリティ:' + str(raw_json['severity']) + '\r\n';
        message += '問題の概要:' + raw_json['description'] + '\r\n';
        message += '詳細情報のリンク:' + raw_json['ciscoDnaEventLink'] ;
    else:
        message = json.dumps(raw_json)


    # uncomment if you are implementing a notifier bot

    api.messages.create(roomId=WT_ROOM_ID, markdown=message)



    # uncomment if you are implementing a controller bot
    '''
    WT_ROOM_ID = raw_json['data']['roomId']
    personEmail_json = raw_json['data']['personEmail']
    if personEmail_json != WT_BOT_EMAIL:
        api.messages.create(roomId=WT_ROOM_ID, markdown=message)
    '''

    return jsonify({'success': True})

if __name__=="__main__":
    app.run()
