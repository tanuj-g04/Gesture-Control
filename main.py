import cv2
import numpy as np
from detector import HandDetector
from gestures import GestureDetector
from actions import VolumeController

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vol_con = VolumeController()
detector = HandDetector()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = detector.find_hands(frame)
    landmarks = detector.get_landmarks(frame)

    if landmarks:
        gesture = GestureDetector(landmarks)
        distance = gesture.distance(4, 8)
        fingers=gesture.fingers_up()
        if fingers==[1,1,0,0,0]:
            volume_level = np.interp(distance, [20, 200], [0, 100])
            vol_con.set_volume(volume_level)

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()