import cv2
import numpy as np
import time

class CircleDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error opening video capture")
            exit()

        self.circle_present = False
        self.circle_start_time = None
        self.real_coordinates = []  # List to store real coordinates

    def get_real_coordinates(self):
        return self.real_coordinates[-1]
    
    def detect_circle(self):
            center_x = center_y = None  # Initialize center_x and center_y
            _, frame = self.cap.read()
            if frame is None:
                print("Error grabbing frame")
                
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
                    if area > 1000:
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        pixel_diameter = 2 * radius
                        real_diameter = 6.3 * 10  # real diameter in mm
                        scale = real_diameter / pixel_diameter  # scale in mm/pixel

                        # Calculate real-world coordinates of the center of the circle
                        center_x = (x - frame.shape[1]//2) * scale
                        center_y = (frame.shape[0]//2 - y) * scale  # Invert the y-coordinate

                        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
                        cv2.putText(frame, f"Pixel Coordinates: ({x:.2f}, {y:.2f})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, f"Real Coordinates: ({center_x:.2f} mm, {center_y:.2f} mm)", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if center_x is not None and center_y is not None:
                        if not self.circle_present:
                            self.circle_present = True
                            self.circle_start_time = time.time()
                            self.temp_coordinates = [(center_x, center_y)]  # Reset the temporary list
                        else:
                            countdown = max(0, int(3 - (time.time() - self.circle_start_time)))
                            cv2.putText(frame, f"Countdown: {countdown}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                            if countdown == 0:
                                cv2.imwrite('screenshot.png', frame)
                                self.circle_present = False
                                # Calculate the average of the x and y values
                                avg_x = sum(x for x, y in self.temp_coordinates) / len(self.temp_coordinates)
                                avg_y = sum(y for x, y in self.temp_coordinates) / len(self.temp_coordinates)
                                self.real_coordinates.append((avg_x, avg_y))  # Store the average coordinates
                                # Print real coordinates
                                print(self.get_real_coordinates())
                            else:
                                self.temp_coordinates.append((center_x, center_y))  # Store the current coordinates
            else:
                cv2.putText(frame, "No circle detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                self.circle_present = False

            cv2.imshow("frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()

    

if __name__ == "__main__":
    detector = CircleDetector()
    while True:
        detector.detect_circle()
    
