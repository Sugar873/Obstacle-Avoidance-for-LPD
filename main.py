import mecademicpy.robot as mdr

class Meca500:
    def __init__(self, address):
        self.robot = mdr.Robot()
        self.address = address

    def connect(self):
        self.robot.Connect(address=self.address, disconnect_on_exception=False)

    def activate_and_home(self):
        self.robot.ActivateRobot()
        self.robot.Home()

    def move_joints(self, joint1, joint2, joint3, joint4, joint5, joint6):
        self.robot.MoveJoints(joint1, joint2, joint3, joint4, joint5, joint6)

    def wait_idle(self):
        self.robot.WaitIdle()

    def deactivate_and_disconnect(self):
        self.robot.DeactivateRobot()
        self.robot.Disconnect()
    
if __name__ == "__main__":
    robot = Meca500('192.168.0.100')  # replace with real host
    robot.connect()
    robot.activate_and_home()
    robot.move_joints(0, 0, 0, 0, 0, 0)
    robot.move_joints(0, -60, 60, 0, 0, 0)
    robot.wait_idle()
    robot.deactivate_and_disconnect()
