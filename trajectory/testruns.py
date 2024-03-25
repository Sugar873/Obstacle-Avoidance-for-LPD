from test_1 import TrajectoryTest
import numpy as np

def test_circle_intersection_points():
    line_start = (0, 0, 0)
    line_end = (10, 10, 10)
    circle_center = (5, 5, 5)
    radius = 0.5
    intersection_points = TrajectoryTest.circle_intersection_points(line_start, line_end, circle_center, radius)
    print("Intersection points:", intersection_points)


if __name__ == "__main__":
    test_circle_intersection_points()