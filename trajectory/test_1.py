import numpy as np
from shapely.geometry import LineString

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

def circle_instersection_points(line_start, line_end, circle_center, radius):
    # Unpack line coordinates
    x0, y0, z0 = line_start
    dx, dy, dz = line_end[0] - x0, line_end[1] - y0, line_end[2] - z0
    
    # Unpack circle coordinates
    cx, cy, cz = circle_center
    
    # Calculate coefficients for the quadratic equation
    a = dx**2 + dy**2 + dz**2
    b = 2 * (dx * (x0 - cx) + dy * (y0 - cy) + dz * (z0 - cz))
    c = (x0 - cx)**2 + (y0 - cy)**2 + (z0 - cz)**2 - radius**2
    
    # Calculate discriminant
    discriminant = b**2 - 4*a*c
    
    # If discriminant is negative, no intersection
    if discriminant < 0:
        return None
    
    # Otherwise, calculate t values
    t1 = (-b + np.sqrt(discriminant)) / (2*a)
    t2 = (-b - np.sqrt(discriminant)) / (2*a)
    
    # Calculate intersection points
    intersection_points = []
    for t in [t1, t2]:
        if 0 <= t <= 1:
            intersection_points.append((x0 + t*dx, y0 + t*dy, z0 + t*dz))
    
    return intersection_points

