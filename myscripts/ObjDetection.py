import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
# this is so if the video capture is not opened, the program will exit
if not cap.isOpened():
    print("Error opening video capture")
    exit()

circle_present = False
circle_start_time = None

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 66, 167])
    upper_blue = np.array([255, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Adjust the area threshold as needed
                (x, y), radius = cv2.minEnclosingCircle(contour)
                pixel_diameter = 2 * radius
                real_diameter = 6.3  # real diameter in cm
                scale = real_diameter / pixel_diameter  # scale in cm/pixel

                # Calculate real-world coordinates of the center of the circle
                center_x = (x - frame.shape[1]//2) * scale
                center_y = (frame.shape[0]//2 - y) * scale  # Invert the y-coordinate

                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                cv2.putText(frame, f"Pixel Coordinates: ({x:.2f}, {y:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, f"Real Coordinates: ({center_x:.2f} cm, {center_y:.2f} cm)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                if not circle_present:
                    circle_present = True
                    circle_start_time = time.time()
                else:
                    countdown = max(0, int(5 - (time.time() - circle_start_time)))
                    cv2.putText(frame, f"Countdown: {countdown}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                    if countdown == 0:
                        cv2.imwrite('screenshot.png', frame)
                        circle_present = False
    else:
        cv2.putText(frame, "No circle detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        circle_present = False

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()