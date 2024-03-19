import cv2
import numpy as np

cap = cv2.VideoCapture(0)
# this is so if the video capture is not opened, the program will exit
if not cap.isOpened():
    print("Error opening video capture")
    exit()

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
                (x, y, w, h) = cv2.boundingRect(contour)
                center_x = int(x + w/2) - frame.shape[1]//2
                center_y = frame.shape[0]//2 - int(y + h/2)  # Invert the y-coordinate
                cv2.circle(frame, (int(x + w/2), int(y + h/2)), int((w + h)/4), (0, 0, 255), 2)
                cv2.putText(frame, f"Coordinates: ({center_x}, {center_y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "No circle detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()