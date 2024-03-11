import pyrealsense2 as rs
import numpy as np

class RealSenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

    def start(self):
        self.pipeline.start(self.config)

    def get_frame(self):
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            return None
        return np.asanyarray(depth_frame.get_data())

    def stop(self):
        self.pipeline.stop()

    def calculate_distance(self, frame):
        return np.mean(frame)

camera = RealSenseCamera()
camera.start()
try:
    while True:
        frame = camera.get_frame()
        if frame is not None:
            distance = camera.calculate_distance(frame)
            print("Distance:", distance)
finally:
    camera.stop()