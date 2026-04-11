import cv2
from detector import HandDetector

cap=cv2.VideoCapture(0)
print("Camera opened: ", cap.isOpened())
detector=HandDetector()

while True:
    ret, frame=cap.read()
    frame=cv2.flip(frame, 1)
    if not ret:
        break
    try:
        frame=detector.find_hands(frame, True)
        landmarks=detector.get_landmarks(frame)
    except Exception as e:
        print("Error: ", e)
        break
    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
