import numpy as np

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