import serial

def get_depth(serial_port: str):
    with serial.Serial(serial_port, 115200) as ser:
        dist_a = ser.readline()
        dist_a = dist_a.decode('utf-8').strip()
        dist_b = ser.readline()
        dist_b = dist_b.decode('utf-8').strip()
        dist_c = ser.readline()
        dist_c = dist_c.decode('utf-8').strip()

        if (abs(dist_b - dist_a) < 2) and (abs(dist_b - dist_c) > 2):
            depth =  (dist_a + dist_b) / 2
        elif (abs(dist_b - dist_a) > 2) and (abs(dist_b - dist_c) < 2):
            depth =  (dist_b + dist_c) / 2
    return depth