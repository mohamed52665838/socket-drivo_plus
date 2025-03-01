import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import asyncio
from global_keys import DATE_TIME_KEY
from global_keys import SLEEP_TIME_TH_SECONDS
from global_keys import SLEEP_MESSAGE_ALERT

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Eye landmarks (Left & Right)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye_points, landmarks):
    A = np.linalg.norm(landmarks[eye_points[1]] - landmarks[eye_points[5]])  
    B = np.linalg.norm(landmarks[eye_points[2]] - landmarks[eye_points[4]])  
    C = np.linalg.norm(landmarks[eye_points[0]] - landmarks[eye_points[3]])  # Horizontal distance
    ear = (A + B) / (2.0 * C)
    return ear


async def proccessImage(frame, writer: asyncio.StreamWriter , last_time_s: dict[str, datetime]):
    # if we need to process opencv 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process with MediaPipe
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) for lm in face_landmarks.landmark])

            left_ear = eye_aspect_ratio(LEFT_EYE, landmarks)
            right_ear = eye_aspect_ratio(RIGHT_EYE, landmarks)

            avg_ear = (left_ear + right_ear) / 2.0

            EAR_THRESHOLD = 0.25
            if avg_ear < EAR_THRESHOLD:
                print(' client is about to sleep')
                # only statement mutate last_time_s variable which from parent culler TODO
                if last_time_s.get(DATE_TIME_KEY) is None:
                    last_time_s[DATE_TIME_KEY] = datetime.now()
            else:
                last_time_s.clear()
            
            if last_time_s.get(DATE_TIME_KEY) is not None:
                time_client_sleeps = datetime.now() - last_time_s[DATE_TIME_KEY] 
                print(f'client sleeping for {time_client_sleeps} !!')
                if time_client_sleeps >= SLEEP_TIME_TH_SECONDS:
                    print('message sent to the client')
                    writer.write(SLEEP_MESSAGE_ALERT)
                    await writer.drain()



if __name__ == '__main__':
# Start video capture
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = np.array([(lm.x * frame.shape[1], lm.y * frame.shape[0]) for lm in face_landmarks.landmark])

                left_ear = eye_aspect_ratio(LEFT_EYE, landmarks)
                right_ear = eye_aspect_ratio(RIGHT_EYE, landmarks)

                avg_ear = (left_ear + right_ear) / 2.0

                EAR_THRESHOLD = 0.25
                if avg_ear < EAR_THRESHOLD:
                    cv2.putText(frame, "Eyes Closed", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Eyes Open", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Eye Blink Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break





    cap.release()
    cv2.destroyAllWindows()
