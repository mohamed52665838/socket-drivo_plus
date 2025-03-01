import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime
import asyncio
from vars import DATE_TIME_KEY

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
EAR_THRESHOLD = 0.25

def eye_aspect_ratio(eye_points, landmarks):
    A = np.linalg.norm(landmarks[eye_points[1]] - landmarks[eye_points[5]])  
    B = np.linalg.norm(landmarks[eye_points[2]] - landmarks[eye_points[4]])  
    C = np.linalg.norm(landmarks[eye_points[0]] - landmarks[eye_points[3]])  # Horizontal distance
    ear = (A + B) / (2.0 * C)
    return ear

def process_image(image, seen_sleepy: dict[str, datetime]):
    frame_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = np.array([(lm.x * image.shape[1], lm.y * image.shape[0]) for lm in face_landmarks.landmark])

            left_ear = eye_aspect_ratio(LEFT_EYE, landmarks)
            right_ear = eye_aspect_ratio(RIGHT_EYE, landmarks)

            avg_ear = (left_ear + right_ear) / 2.0

            if avg_ear < EAR_THRESHOLD:
                # only statement mutate last_time_s variable which from parent culler TODO
                if seen_sleepy.get(DATE_TIME_KEY) is None:
                    seen_sleepy[DATE_TIME_KEY] = datetime.now()
            else:
                seen_sleepy.clear()
