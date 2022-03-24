#!/usr/bin/env python

import asyncio
import enum
import websockets
import json
import random
from datetime import datetime

users = {
    0 : 'A',
    1 : 'B'
}
clients = dict()
msgs = []
emotions = ["ALORS", "Y A PAS ENCORE D?EMOTIONS", "MAIS çA ARRIVE"]


async def error(websocket, message):
    """
    Send an error message.

    """
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def handler(websocket):
    if len(clients.keys()) > 2 :
        print('connection refused')
    else :
        id = len(clients.keys())
        await websocket.send(f"connected {id}")
        print(f"{id} connected")
        clients[id] = websocket
        while True:
            try:
                # type : cmd, txt, 
                # msg = {'userid' : 1, 'type' : 'get_msgs', 'data': data, 'clear' 
                message = await websocket.recv() 
                print(f'message : {message}')
                json_msg = json.loads(message)
                print(f'json msg : {json_msg}')
                if json_msg['type'] == 'cmd':
                    if json_msg['data'] == 'clear':
                        msgs.clear()
                    await send_msgs(websocket)
                elif json_msg['type'] == 'txt':
                    msgs.append({"text" :json_msg['data'], "userid" :json_msg['userid'], "timestamp": datetime.now().strftime("%H:%M:%S")})
                    for id in clients :
                        await send_msgs(clients[id])

            except websockets.ConnectionClosedOK:
                print(f"Client {id} disconnected")
                clients[id].close()
                clients.pop(id)
                break

async def send_msgs(websocket):
    await websocket.send(json.dumps({"msgs" : msgs, "emotions": compute_emotions()}))

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8002):
        await asyncio.Future()  # run forever

def compute_emotions():
    # msg = text, userid, timestamp
    result = ''
    for msg in msgs :
        tmp = users[msg['userid']] + ' : ' + msg['text'] + '\n'
        result += tmp

    # TODO : CALL GP3T
    print(f'result : {result}')
    return result

if __name__ == "__main__":
    asyncio.run(main())