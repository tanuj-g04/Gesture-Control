import cv2
import numpy as np
from detector import HandDetector
from gestures import GestureDetector
from actions import VolumeController
from actions import BrightnessController
from actions import MouseController
import comtypes
import pyautogui
comtypes.CoInitialize()
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
pyautogui.MINIMUM_DURATION = 0

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
vol_con = VolumeController()
detector = HandDetector()
bri_con = BrightnessController()
mouse = MouseController()
prev_distance=0
prev_x = None
prev_y = None
click_cooldown = 0
threshold=5

while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("no frame")
            continue
        frame = cv2.flip(frame, 1)
        frame = detector.find_hands(frame)
        frame_h, frame_w,_ = frame.shape
        landmarks = detector.get_landmarks(frame)
        if landmarks:
            gesture = GestureDetector(landmarks)
            fingers=gesture.fingers_up()
            
            if fingers==[0,1,1,0,0]:
                curr_x = landmarks[8][1]
                if prev_x is not None:
                    if curr_x > prev_x + threshold:
                        vol_con.change_volume("up")
                    elif curr_x < prev_x - threshold:
                        vol_con.change_volume("down")
                prev_x = curr_x
                
            
            if fingers == [0,0,0,0,1]:
                curr_y = landmarks[20][2]  # pinky tip y position
                if prev_y is not None:
                    if curr_y < prev_y - threshold:  # moving up = brighter
                        bri_con.change_brightness("up")
                    elif curr_y > prev_y + threshold:
                        bri_con.change_brightness("down")
                prev_y = curr_y

            if fingers == [0,1,0,0,0]:
                x,y = landmarks[8][1], landmarks[8][2]
                mouse.move(x, y, frame_w, frame_h)

            if fingers[1] == 1:  # index up = mouse mode active
                hand_size = gesture.distance(0, 5)          # wrist to index-base
                pinch_ratio = gesture.distance(4, 8) / hand_size

                if pinch_ratio < 0.3 and click_cooldown == 0:
                    mouse.click()
                    click_cooldown = 10

                if click_cooldown > 0:
                    click_cooldown -= 1           

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