

import asyncio
from websockets.asyncio.client import connect
import cv2
from vars import SERVER_ADDRESS, SERVER_PORT
cap = cv2.VideoCapture(0)  

async def send_frames(websocket):
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Failed to capture frame")
                    break
                
                frame = cv2.resize(frame, dsize=(120, 120))

                _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
                img_bytes = buffer.tobytes()
                await websocket.send(img_bytes)
                await asyncio.sleep(0.05) # 20 frame per second
        except Exception as e:
            print(f"Client stopped: {e}")
        
        finally:
            cap.release()


async def receive_message(websocket):
    async for message in websocket:
        print(f'we have message from the server {message}')

async def send_and_receive():
    async with connect(f'ws://{SERVER_ADDRESS}:{SERVER_PORT}') as websocket:
        await asyncio.gather(send_frames(websocket), receive_message(websocket))


if __name__ == "__main__":
    asyncio.run(send_and_receive())