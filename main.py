import cv2
import numpy as np
from detector import HandDetector
from gestures import GestureDetector
from actions import VolumeController
from actions import BrightnessController
import comtypes
comtypes.CoInitialize()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vol_con = VolumeController()
detector = HandDetector()
bri_con = BrightnessController()
prev_distance=0
threshold=5

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("no frame")
            continue
        frame = cv2.flip(frame, 1)
        frame = detector.find_hands(frame)
        landmarks = detector.get_landmarks(frame)
        if landmarks:
            gesture = GestureDetector(landmarks)
            fingers=gesture.fingers_up()
            if fingers==[1,1,0,0,0]:
                distance = gesture.distance(4, 8)
                if distance > prev_distance + threshold:
                    vol_con.change_volume("up")
                elif distance < prev_distance - threshold:
                    vol_con.change_volume("down")
                prev_distance=distance
            if fingers==[0,1,1,0,0]:
                distance = gesture.distance(8,12)
                if distance > prev_distance + threshold:
                    bri_con.change_brightness("up")
                elif distance < prev_distance - threshold:
                    bri_con.change_brightness("down")
                prev_distance=distance
        cv2.imshow("Gesture Control", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("break: q pressed")
            break
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("break: exception")
        break

cap.release()
cv2.destroyAllWindows()