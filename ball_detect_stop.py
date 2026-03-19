
import cv2
import numpy as np
import requests
import time

STREAM_URL = "http://192.168.4.1:81/stream"
STOP_URL = "http://192.168.4.1/stop"

last_stop_time = 0
STOP_COOLDOWN = 2

cap = cv2.VideoCapture(STREAM_URL)

if not cap.isOpened():
    print("Could not connect to camera stream")
    exit()

print("Connected to stream. Press q to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No frame received")
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (9, 9), 2)

    circles = cv2.HoughCircles(
        mask,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=50,
        param1=100,
        param2=20,
        minRadius=10,
        maxRadius=120
    )

    detected_ball = False
    ball_radius = 0

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        biggest = max(circles, key=lambda c: c[2])
        x, y, r = biggest
        ball_radius = r
        detected_ball = True

        cv2.circle(frame, (x, y), r, (0, 255, 0), 3)
        cv2.circle(frame, (x, y), 3, (255, 0, 0), -1)
        cv2.putText(frame, f"Ball detected r={r}", (x - 40, y - r - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    if detected_ball and ball_radius >= 30:
        now = time.time()
        if now - last_stop_time > STOP_COOLDOWN:
            try:
                response = requests.get(STOP_URL, timeout=1)
                print(f"STOP sent: {response.status_code}")
                last_stop_time = now
            except Exception as e:
                print("STOP request failed:", e)

    cv2.imshow("Ball Detect Stop", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
