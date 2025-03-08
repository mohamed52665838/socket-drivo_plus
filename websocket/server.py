import json
import asyncio
import cv2
import numpy as np
from websockets.asyncio.server import serve
from datetime import datetime
import base64
from vars import SERVER_ADDRESS, SERVER_PORT, DATE_TIME_KEY, SLEEP_MESSAGE_ALERT, SLEEP_THREASHOLD, SEND_NOTIFICATION_KEY, NOTIFICAITON_CAT, NOTIFICATION_SERVICE_ADDRESS, NOTIFICATION_SERVICE_PORT,NO_FACE_KEY , NO_FACE_THREASHOLD, NO_FACE_ALERT, VAR_CONF
from app_types import NotificationBody
from process_websocket import process_image
from dataclasses import asdict
import aiohttp
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)  # Change level as needed
from vars import SLEEP_THREASHOLD, NO_FACE_THREASHOLD, APP_PORT, NOTIFICATION_SERVICE_PORT

logging.info("IMPORTANT INFO".center(50, "="))
logging.info(f"Application Listen inside the container (APP_PORT) {APP_PORT}")
logging.info(f"Communicate with Notification service on (NOTIFICATION_SERVICE_PORT) {NOTIFICATION_SERVICE_PORT}")
logging.info(f"With Sleep Threshhold (SLEEP_TIME_ALERT) {SLEEP_THREASHOLD}s")
logging.info(f"With Miss Face Threshhold (NF_TIME_ALERT) {NO_FACE_THREASHOLD}s")
logging.info(f"=" * 50)
logging.info(f"Var Conf (CONF_VAR): {VAR_CONF}")
logging.info("="*50)

async def send_notification(notification: NotificationBody, info_related: dict[str, datetime | str]):

    last_time_send_notification = info_related.get(SEND_NOTIFICATION_KEY)
    
    try:
        delta_time = datetime.now() - last_time_send_notification
        if delta_time.seconds < 10:
            # we don't need to send notification each second !
            return
    except TypeError:
        pass

    async with aiohttp.ClientSession() as session:
        url = f"http://{NOTIFICATION_SERVICE_ADDRESS}:{NOTIFICATION_SERVICE_PORT}/notifications/send_notification"
        
        async with session.post(url, json=asdict(notification), headers={'Content-Type': 'application/json'}) as response:
            print(response.status)
            data_back = await response.json()
            print(data_back)
            if response.status == 200 and data_back is not None:
                if data_back.get('data') is not None and data_back.get('data').get('status') == 'error':
                    print(f"Request Failed: {data_back.get('data').get('message')}")
                    print(f"Details: {data_back.get('data').get('details')}")
                    return
             



async def server_data(websocket):
    last_time_sleep: dict[str , datetime] = {}
    handshake_message = await websocket.recv()
    handshake_data: dict 
    try:
        handshake_data = json.loads(handshake_message)
        if handshake_data.get("user_id") is None or handshake_data.get('token') is None:
            await websocket.close()
            return
    except json.JSONDecodeError:
        print("Invalid handshake format. Closing connection.")
        await websocket.close()
        return
    async for message in websocket:
            if message and isinstance(message, str):
                data = base64.b64decode(message)
                image_bytes = np.asarray(bytearray(data), dtype=np.uint8)
                img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

                try:
                    process_image(image=img, extra_data=last_time_sleep)    
                    last_time = last_time_sleep.get(DATE_TIME_KEY)

                    if last_time:
                        delta_sleep = datetime.now() - last_time
                        print(f'delta sleep time is {delta_sleep}')
                        if delta_sleep.seconds > SLEEP_THREASHOLD:
                            res = await websocket.send(SLEEP_MESSAGE_ALERT)
                            last_time_sleep.pop(DATE_TIME_KEY) 
                            requestBody = NotificationBody(category='physical_alert', user_id=handshake_data.get('user_id'),token=handshake_data.get('token'))
                            await send_notification(requestBody, last_time_sleep)
                            print(f'sleep alert sent')
                    
                    no_face_exits = last_time_sleep.get(NO_FACE_KEY)
                    if no_face_exits:
                        delta_sleep_nf = datetime.now() - no_face_exits
                        if delta_sleep_nf.seconds > NO_FACE_THREASHOLD:
                            await websocket.send(NO_FACE_ALERT)
                            last_time_sleep.pop(NO_FACE_KEY) 
                            requestBody = NotificationBody(category='montal_alert', user_id=handshake_data.get('user_id'),token=handshake_data.get('token'))
                            await send_notification(requestBody, last_time_sleep)
                            print(f'No face alert sent')
                    
                except KeyboardInterrupt:
                    websocket.close()
                except Exception as e:
                    print(e.args)

async def main():
    async with serve(server_data, SERVER_ADDRESS, int(APP_PORT), ping_interval=None) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())