import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands=mp.solutions.hands
        self.hands=self.mp_hands.Hands(max_num_hands= max_hands, min_detection_confidence=detection_confidence, min_tracking_confidence=tracking_confidence)
        self.mp_draw=mp.solutions.drawing_utils
    
    def find_hands(self, frame, draw=True):
        frame_rgb=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results=self.hands.process(frame_rgb)
        if self.results.multi_hand_landmarks:
            for hands_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hands_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def get_landmarks(self, frame):
        landmarks=[]
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                for id, lm in enumerate(hand_landmarks.landmark):
                    h, w, c=frame.shape
                    cx, cy= int(lm.x*w), int(lm.y*h)
                    landmarks.append((cx,cy))
        return landmarks