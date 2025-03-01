import socket
import cv2
import struct
import select

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5001  

def send_frames():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")

    cap = cv2.VideoCapture(0)  # Open webcam (0 = default camera)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            _, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
            img_bytes = buffer.tobytes()

            length_header = f"{len(img_bytes):<10}".encode()
            client_socket.send(length_header)  
            client_socket.sendall(img_bytes)  

            ready, _, _ = select.select([client_socket], [], [], 0.1)
            if ready:
                response = client_socket.recv(1024)
                print("Server response:", response.decode())

    except Exception as e:
        print(f"Client stopped: {e}")
    
    finally:
        cap.release()
        client_socket.close()
        cv2.destroyAllWindows()

send_frames()
