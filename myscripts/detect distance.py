import cv2
import pyrealsense2
from realsense_depth import *

class DistanceDetector:
    def __init__(self):
        self.point = (400, 300)
        self.dc = DepthCamera()
        cv2.namedWindow("Color frame")
        cv2.setMouseCallback("Color frame", self.show_distance)

    def show_distance(self, event, x, y, args, params):
        self.point = (x, y)

    def run(self):
        while True:
            ret, depth_frame, color_frame = self.dc.get_frame()

            cv2.circle(color_frame, self.point, 4, (0, 0, 255))
            distance = depth_frame[self.point[1], self.point[0]]

            cv2.putText(color_frame, "{}m".format(distance/1000), (self.point[0], self.point[1] - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

            cv2.imshow("depth frame", depth_frame)
            cv2.imshow("Color frame", color_frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

if __name__ == "__main__":
    detector = DistanceDetector()
    detector.run()
