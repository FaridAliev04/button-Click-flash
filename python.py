from cvzone.HandTrackingModule import HandDetector
import cv2
from arduino_control import ArduinoController
import math

arduino = ArduinoController(port='COM4', baudrate=9600)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)  

circles = [
    {"center": (150, 200), "radius": 50, "filled": False},
    {"center": (350, 200), "radius": 50, "filled": False},
    {"center": (550, 200), "radius": 50, "filled": False}
]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    for circle in circles:
        circle["filled"] = False

    if hands:
        for hand in hands:  
            lmList = hand["lmList"]
            index_tip = lmList[8]  
            ix, iy = index_tip[0], index_tip[1]

            min_dist = float('inf')
            selected_circle = None
            for circle in circles:
                cx, cy = circle["center"]
                dist = math.hypot(ix - cx, iy - cy)
                if dist < min_dist:
                    min_dist = dist
                    selected_circle = circle

            if min_dist < 80:  
                selected_circle["filled"] = True
            cv2.circle(img, (ix, iy), 10, (255, 0, 0), cv2.FILLED)
    led_states = ''.join(['1' if c["filled"] else '0' for c in circles])
    arduino.send_led_states(led_states)
    
    for circle in circles:
        cx, cy = circle["center"]
        r = circle["radius"]
        if circle["filled"]:
            cv2.circle(img, (cx, cy), r, (0, 255, 0), -1)
        else:
            cv2.circle(img, (cx, cy), r, (0, 255, 0), 3)

    cv2.imshow("Two-Hand Finger LED Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
