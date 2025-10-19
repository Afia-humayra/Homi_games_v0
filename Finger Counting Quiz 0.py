import cv2
from cvzone.HandTrackingModule import HandDetector
import random
import time

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

detector = HandDetector(detectionCon=0.8, maxHands=2)

target_number = random.randint(1, 10)
score = 0
last_correct_time = 0
show_correct = False
SWITCH_DELAY = 1.5

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    h, w, _ = img.shape

    cv2.putText(img, f"Show me {target_number} fingers!", (30, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 0), 3)

    cv2.putText(img, f"Score: {score}", (w - 200, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

    totalFingers = 0
    if hands:
        for hand in hands:
            fingers = detector.fingersUp(hand)
            totalFingers += fingers.count(1)

        cv2.putText(img, f'You showed: {totalFingers}', (30, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3)

        if totalFingers == target_number and not show_correct:
            score += 1
            show_correct = True
            last_correct_time = time.time()
        elif totalFingers != target_number and not show_correct and totalFingers != 0:
            cv2.putText(img, "Wrong!", (30, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    if show_correct:
        cv2.putText(img, "Correct!", (30, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        if time.time() - last_correct_time > SWITCH_DELAY:
            target_number = random.randint(1, 10)
            show_correct = False

    cv2.imshow("Finger Counting Quiz", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
