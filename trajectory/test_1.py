import numpy as np
from shapely.geometry import LineString

class TrajectoryTest:

    def create_parametric_line(start_point, end_point, num_points=20):
        # Extract start and end coordinates
        x0, y0, z0 = start_point
        x1, y1, z1 = end_point
        
        # Calculate increments for each coordinate
        dx = (x1 - x0) / (num_points - 1)
        dy = (y1 - y0) / (num_points - 1)
        dz = (z1 - z0) / (num_points - 1)
        
        # Generate parametric line points
        parametric_line = [(x0 + i*dx, y0 + i*dy, z0 + i*dz) for i in range(num_points)]
        
        return parametric_line

    def create_circle_parametric_line(circle_center, radius, num_points=100):
        cx, cy, cz = circle_center
        
        # Generate parametric line points
        parametric_line = []
        for i in range(num_points):
            theta = 2 * np.pi * i / num_points
            x = cx + radius * np.sin(theta)
            y = cy + radius * np.cos(theta)
            parametric_line.append((x, y, cz))  # Circle is in xy-plane, so z-coordinate is constant
        
        return parametric_line

    def edge_intersection_points(points_set, parametric_line):
        line = LineString(parametric_line)
        intersection_points = []

        for i in range(len(points_set) - 1):
            segment = LineString([points_set[i], points_set[i+1]])
            intersection = line.intersection(segment)

            if intersection.is_empty:
                continue
            elif intersection.geom_type == 'Point':
                intersection_points.append((intersection.x, intersection.y, intersection.z))
            elif intersection.geom_type == 'MultiPoint':
                for point in intersection:
                    intersection_points.append((point.x, point.y, point.z))

        return intersection_points

    def circle_intersection_points(start_point, end_point, circle_center, circle_radius):
        # Convert inputs to numpy arrays
        start_point = np.array(start_point)
        end_point = np.array(end_point)
        circle_center = np.array(circle_center)
        
        # Direction vector of the line
        direction = end_point - start_point
        
        # Equation of the circle's plane
        circle_normal = circle_center - start_point
        t = np.dot(circle_normal, circle_center - start_point) / np.dot(direction, circle_normal)
        plane_point = start_point + t * direction
        
        # Distance from the plane point to the circle center
        distance_to_center = np.linalg.norm(plane_point - circle_center)
        
        # Check if the distance is within the circle's radius
        if distance_to_center <= circle_radius:
            # Projection of the plane point onto the circle's plane
            projection = circle_center + np.dot(plane_point - circle_center, circle_normal) / np.dot(circle_normal, circle_normal) * circle_normal
            
            # Calculate the intersection points using the projection and the circle's radius
            if np.allclose(projection, circle_center):
                return [tuple(projection)]
            else:
                chord_length = np.sqrt(circle_radius ** 2 - distance_to_center ** 2)
                intersection1 = projection + chord_length * (end_point - start_point) / np.linalg.norm(end_point - start_point)
                intersection2 = projection - chord_length * (end_point - start_point) / np.linalg.norm(end_point - start_point)
                return [tuple(intersection1), tuple(intersection2)]
        else:
            return []

