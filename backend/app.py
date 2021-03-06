#!/usr/bin/env python

import asyncio
from pandas import lreshape
import websockets
import json
from datetime import datetime
from openapi_test2 import get_emotions
from urllib import parse, request
import random

GOOD_EMOTIONS = ['happy', 'friendly', 'flattered', 'admirative', 'amused', 'caring',
                 'desiring', 'excited', 'grateful', 'joyful', 'loved', 'optimist', 'proud', 'relieved']

BAD_EMOTIONS = ['insulted', 'embarrassed', 'sad', 'angry', 'disrepected', 'ashamed', 'shaken', 'unsafe', 'bullied',
                'unconfortable', 'angry', 'annoyed', 'disappointed', 'disapproved', 'disgusted', 'afraid', 'griving', 'nervous', 'remorse', 'sad']
NEUTRAL_EMOTIONS = ['confused', 'curious', 'realized', 'suprised']
GIPHY_API_KEY = 'pui3355ayqU0UNdFY4Yt6IDiNOrgk2tn'
GIPHY_URL = "http://api.giphy.com/v1/gifs/search"

users = {
    '0': 'A',
    '1': 'B'
}
clients = dict()
msgs = []


async def error(websocket, message):
    print(message)
    """
    Send an error message.

    """
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def handler(websocket):
    if len(clients.keys()) >= 2:
        error_msg = 'connection refused'
        await error(websocket, error_msg)
    else:
        id = len(clients.keys())
        await websocket.send(f"connected {id}")
        print("User " + users[str(id)] + " connected")
        clients[id] = websocket
        while True:
            try:
                # type : cmd, txt,
                # msg = {'userid' : 1, 'type' : 'get_msgs', 'data': data}
                message = await websocket.recv()
                print(f'message : {message}')
                json_msg = json.loads(message)
                print(f'json msg : {json_msg}')
                if json_msg['type'] == 'cmd':
                    if json_msg['data'] == 'clear':
                        msgs.clear()
                    await send_msgs()
                elif json_msg['type'] == 'txt':
                    msgs.append({"text": json_msg['data'], "userid": json_msg['userid'], "timestamp": datetime.now(
                    ).strftime("%H:%M:%S")})
                    await send_msgs()

            except websockets.ConnectionClosedOK:
                print("User " + users[str(id)] + " disconnected")
                clients[id].close()
                clients.pop(id)
                break

async def send_msgs():
    for id in clients:
        await clients[id].send(json.dumps({"msgs": msgs}))
    for id in clients:
        raw_data = compute_emotions()
        raw_data = [s[1:] for s in raw_data]
        print(f'raw_data : {raw_data}')
        a_feeling = raw_data[0].split()[-1]
        b_feeling = raw_data[1].split()[-1]
        a_gif_url = get_GIF_url(a_feeling)
        b_gif_url = get_GIF_url(b_feeling)
        await clients[id].send(json.dumps({"emotions": raw_data, "A_gif_url": a_gif_url, "B_gif_url": b_gif_url}))


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8002):
        await asyncio.Future()  # run forever


def get_GIF_url(feeling):
    
    #f = open('URL_GIFs.json')
    #url_gifs = json.load(f)
    #if feeling in url_gifs.keys():
    #    return url_gifs[feeling]
    #else :
    params = parse.urlencode({
    "q": feeling,
    "api_key": GIPHY_API_KEY,
    "limit": "10"
    })

    with request.urlopen("".join((GIPHY_URL, "?", params))) as response:
        data = json.loads(response.read())

    rdm_gif = random.randint(0, 9)
    id = data['data'][rdm_gif]['id']
    url = 'https://i.giphy.com/media/' + id +'/giphy.webp'
    return url

def compute_emotions():
    # msg = text, userid, timestamp
    conversation = ''
    for msg in msgs:
        tmp = users[msg['userid']] + ': ' + msg['text'] + '\n'
        conversation += tmp

    return get_emotions(conversation)

if __name__ == "__main__":
    asyncio.run(main())
