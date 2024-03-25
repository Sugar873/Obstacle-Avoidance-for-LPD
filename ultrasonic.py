import serial

class Ultrasonic:
    def __init__(self, serial_port, baud_rate):
        self.ser = serial.Serial(serial_port, baud_rate)

    def get_depth(self):   
        dist_a = self.ser.readline()
        dist_a = int(dist_a.decode('utf-8').strip())
        dist_b = self.ser.readline()
        dist_b = int(dist_b.decode('utf-8').strip())
        dist_c = self.ser.readline()
        dist_c = int(dist_c.decode('utf-8').strip())

        if (abs(dist_b - dist_a) <= 2) and (abs(dist_b - dist_c) > 2):
            depth =  (dist_a + dist_b) / 2
        elif (abs(dist_b - dist_a) > 2) and (abs(dist_b - dist_c) <= 2):
            depth =  (dist_b + dist_c) / 2
        else:
            depth = dist_b
        return int(depth)