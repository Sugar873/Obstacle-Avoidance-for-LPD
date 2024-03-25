import numpy as np
# Convert (hard coded) constraint points from Camera Frame to WRF

class TransformRobot:
    def __init__(self):
        self.a = [0, 0, 0, 0, 0, 0]
        self.d = [0, 0, 0, 0, 0, 0]
        self.alpha = [0, 0, 0, 0, 0, 0]
        self.theta = [0, 0, 0, 0, 0, 0]
    
    def get_fwd_kin(self, a=None, d=None, alpha=None, theta=None):
        if a is not None and d is not None and alpha is not None and theta is not None:
            self.set_a(a)
            self.set_d(d)
            self.set_alpha(alpha)
            self.set_theta(theta)

        i = 0
        T01 = np.array([[np.cos(self.theta[i]), -np.sin(self.theta[i])*np.cos(self.alpha[i]), np.sin(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.cos(self.theta[i])], \
                    [np.sin(self.theta[i]), np.cos(self.theta[i])*np.cos(self.alpha[i]), -np.cos(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.sin(self.theta[i])], \
                    [0, np.sin(self.alpha[i]), np.cos(self.alpha[i]), self.d[i]],
                    [0,0,0,1]])
        
        i = 1
        T12 = np.array([[np.cos(self.theta[i]), -np.sin(self.theta[i])*np.cos(self.alpha[i]), np.sin(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.cos(self.theta[i])], \
                    [np.sin(self.theta[i]), np.cos(self.theta[i])*np.cos(self.alpha[i]), -np.cos(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.sin(self.theta[i])], \
                    [0, np.sin(self.alpha[i]), np.cos(self.alpha[i]), self.d[i]],
                    [0,0,0,1]])
        i = 2
        T23 = np.array([[np.cos(self.theta[i]), -np.sin(self.theta[i])*np.cos(self.alpha[i]), np.sin(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.cos(self.theta[i])], \
                    [np.sin(self.theta[i]), np.cos(self.theta[i])*np.cos(self.alpha[i]), -np.cos(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.sin(self.theta[i])], \
                    [0, np.sin(self.alpha[i]), np.cos(self.alpha[i]), self.d[i]],
                    [0,0,0,1]])

        i = 3
        T34 = np.array([[np.cos(self.theta[i]), -np.sin(self.theta[i])*np.cos(self.alpha[i]), np.sin(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.cos(self.theta[i])], \
                    [np.sin(self.theta[i]), np.cos(self.theta[i])*np.cos(self.alpha[i]), -np.cos(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.sin(self.theta[i])], \
                    [0, np.sin(self.alpha[i]), np.cos(self.alpha[i]), self.d[i]],
                    [0,0,0,1]])

        i = 4
        T45 = np.array([[np.cos(self.theta[i]), -np.sin(self.theta[i])*np.cos(self.alpha[i]), np.sin(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.cos(self.theta[i])], \
                    [np.sin(self.theta[i]), np.cos(self.theta[i])*np.cos(self.alpha[i]), -np.cos(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.sin(self.theta[i])], \
                    [0, np.sin(self.alpha[i]), np.cos(self.alpha[i]), self.d[i]],
                    [0,0,0,1]])

        i = 5
        T56 = np.array([[np.cos(self.theta[i]), -np.sin(self.theta[i])*np.cos(self.alpha[i]), np.sin(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.cos(self.theta[i])], \
                    [np.sin(self.theta[i]), np.cos(self.theta[i])*np.cos(self.alpha[i]), -np.cos(self.theta[i])*np.sin(self.alpha[i]), self.a[i]*np.sin(self.theta[i])], \
                    [0, np.sin(self.alpha[i]), np.cos(self.alpha[i]), self.d[i]],
                    [0,0,0,1]])     

        print(T01)
        print(T12)
        print(T23)
        print(T34)
        print(T45)
        print(T56)
        M = T01 @ T12 @ T23 @ T34 @ T45 @ T56
        return M
    
    def extract_euler(self, rotation_matrix) -> tuple:
        alpha = 0
        beta = 0
        gamma = 0

        if abs(rotation_matrix[0,2]) > 0.99 and abs(rotation_matrix[0,2]) < 1.01:
            beta = np.pi / 2
            alpha = np.arctan2(rotation_matrix[1, 0], rotation_matrix[1,1])
            gamma = 0
        else:
            beta = np.arcsin(rotation_matrix[0,2])
            alpha = np.arctan2(-rotation_matrix[1,2], rotation_matrix[2,2])
            gamma = np.arctan2(-rotation_matrix[0,1], rotation_matrix[0,0])

        return (alpha, beta, gamma)
    
    def extract_position(self, rotation_matrix) -> tuple:
        x = rotation_matrix[0,3]
        y = rotation_matrix[1,3]
        z = rotation_matrix[2,3]
        return (x, y, z)
    
    def set_a(self, a):
        self.a = a
    
    def set_d(self, d):
        self.d = d

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_theta(self, theta):
        self.theta = theta

class TransformConstraint:
    def __init__(self):
        self.constr_arr = []

    def transform_constraint(self, constr_pos: tuple, cam_cart: tuple) -> tuple:
        """
        Transform from Camera Reference Frame (CRF) to World Reference Frame (WRF)
        constr_pos is a tuple of (x,y,z) position of obstacle obtained from depth camera.
        cam_cart is the tuple of the cartesian coordinates (x, y, z, alpha, beta, gamma) 
            initially set beforehand.
        """
        x, y, z, a, b, g = cam_cart
        a = a * (np.pi/180)
        b = b * (np.pi/180)
        g = g * (np.pi/180)
        X, Y, Z = constr_pos

        target_coord = np.array([[X], [Y], [Z], [1]])
        # This s using the Meca500 convention via current axes (Rx Ry Rz)
        T = np.array([[np.cos(a)*np.sin(b), np.cos(a)*np.sin(b)*np.sin(g)-np.sin(a)*np.cos(g), np.cos(a)*np.sin(b)*np.cos(g)+np.sin(a)*np.sin(g),x], \
            [np.sin(a)*np.cos(b), np.sin(a)*np.sin(b)*np.sin(g)+np.cos(a)*np.cos(g), np.sin(a)*np.sin(b)*np.cos(g)-np.cos(a)*np.sin(g), y], \
            [-np.sin(b), np.cos(b)*np.sin(g), np.cos(b)*np.cos(g), z],
            [0,0,0,1]])

        # This is using the normal convention via fixed axes (Rz Ry Rx)
        # T = np.array([[np.cos(b)*np.cos(g), np.sin(a)*np.sin(b)*np.cos(g)-np.cos(a)*np.sin(g), np.cos(a)*np.sin(b)*np.cos(g)+np.sin(a)*np.sin(g),x], \
        #     [np.cos(b)*np.sin(g), np.sin(a)*np.sin(b)*np.sin(g)+np.cos(a)*np.cos(g), np.cos(a)*np.sin(b)*np.sin(g)-np.sin(a)*np.cos(g), y], \
        #     [-np.sin(b), np.sin(a)*np.cos(b), np.cos(a)*np.cos(b), z],
        #     [0,0,0,1]])
        
        # Get the point w.r.t WRF using matrix multiplication
        P = T @ target_coord

        # Return the coordinates of the same point w.r.t WRF
        new_point = [x[0] for x in P]
        self._add_constr_to_arr((round(new_point[0], 2), round(new_point[1], 2), round(new_point[2], 2)))
        return (round(new_point[0], 2), round(new_point[1], 2), round(new_point[2], 2))


    def _add_constr_to_arr(self, constr_coord):
        self.constr_arr += [constr_coord]
        return self.constr_arr

    def get_constr_arr(self):
        return self.constr_arr


# if __name__ == "__main__":
    # proc = TransformConstraint()

    # Dummy values - for testing
    # constraint = (1,1,1)
    # camera = (0,10,10,90,90,0)
    # constraint_in_wrf = proc.transform_constraint(constraint, camera)
    # arr = proc.add_constr_to_arr(constraint_in_wrf)
    # print(constraint_in_wrf)
    # print(proc.get_constr_arr())

    # constraint = (5,1,5)
    # camera = (-10,10,5,0,90,0)
    # constraint_in_wrf = proc.transform_constraint(constraint, camera)
    # arr = proc.add_constr_to_arr(constraint_in_wrf)
    # print(constraint_in_wrf)
    # print(proc.get_constr_arr())

#     constraint = (142.5883, -64.2218, -110.733)
#       get forward kin where the camera is
#       extract x, y, z, alpha, beta, gamma then input it in the transform
#     camera = (150,-75,190,-45,45,45)
#     constraint_in_wrf = proc.transform_constraint(constraint, camera)
#     arr = proc.add_constr_to_arr(constraint_in_wrf)
#     print(constraint_in_wrf)
#     print(arr)

#     const = proc.get_constr_arr()
#     print(const)

