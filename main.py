import asyncio
import cv2
import numpy as np
import io
from datetime import datetime
from drownsiness_process import proccessImage # camelcase not recommended !!

# Socket Gobals
HOST = "0.0.0.0"
PORT = 5001
TIMEOUT_SECONDS = 8 # HELLO THERE FIVE SECOND THATS IT !!


async def handle_client(reader, writer):
    counter = 0 # each client has counter 
    addr = writer.get_extra_info("peername")
    print(f"Connected by {addr}")

    # global variable to each client
    last_time_sleep: dict[str , datetime] = {}

    try:
        while True:
            if counter % 100 == 0:
                print(f'we have {counter} frame from {addr}')
            counter += 1
            length_header = await asyncio.wait_for(reader.readexactly(10), timeout=TIMEOUT_SECONDS)
            frame_length = int(length_header.decode().strip())

            buffer = io.BytesIO()
            buffer.write(await asyncio.wait_for(reader.readexactly(frame_length), timeout=TIMEOUT_SECONDS))

            buffer.seek(0) 
            image_bytes = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
            img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
            await proccessImage(frame=img, writer=writer, last_time_s=last_time_sleep) 

    except asyncio.TimeoutError:
        print(f"Timeout: No data received from {addr} for {TIMEOUT_SECONDS} seconds. Closing connection.")

    except asyncio.IncompleteReadError:
        print(f"Client {addr} disconnected.")

    except Exception as e:
        # TODO identify all kind of error may happen
        print(f'unexpected error just happned to client {e}')
        print(f'type of error is {type(e)}')

    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Listening on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
