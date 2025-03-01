
import asyncio
import cv2
import numpy as np
from websockets.asyncio.server import serve
from datetime import datetime
import base64
from vars import SERVER_ADDRESS, SERVER_PORT, DATE_TIME_KEY, SLEEP_MESSAGE_ALERT
from process_websocket import process_image



async def server_data(websocket):
    last_time_sleep: dict[str , datetime] = {}
    async for message in websocket:
            if message and isinstance(message, str):
                data = base64.b64decode(message)
                image_bytes = np.asarray(bytearray(data), dtype=np.uint8)
                img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)

                try:
                    process_image(image=img, seen_sleepy=last_time_sleep)    
                    last_time = last_time_sleep.get(DATE_TIME_KEY)

                    if last_time:
                        delta_sleep = datetime.now() - last_time
                        if delta_sleep.seconds > 3:
                            res = await websocket.send(SLEEP_MESSAGE_ALERT)
                            
                            print(f'message sent to client {res}')

                        print(f'client is sleeping since {delta_sleep}')
                        
                
                except KeyboardInterrupt:
                    websocket.close()
                except Exception as e:
                    print(e)

async def main():
    async with serve(server_data, SERVER_ADDRESS, SERVER_PORT, ping_interval=None) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())