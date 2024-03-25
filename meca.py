import mecademicpy.robot as mdr

"""
https://github.com/Mecademic/mecademicpy/blob/main/mecademicpy/robot.py
"""

class MecaRobot:
    def __init__(self, address):
        self.robot = mdr.Robot()
        self.address = address
        self.callbacks = mdr.RobotCallbacks()
        self.register_callbacks()

    def register_callbacks(self):
        self.callbacks.on_connected = lambda: self.on_event("Connected")
        self.callbacks.on_disconnected = lambda: self.on_event("Disconnected")
        self.callbacks.on_activated = lambda: self.on_event("Activated")
        self.callbacks.on_deactivated = lambda: self.on_event("Deactivated")
        self.callbacks.on_homed = lambda: self.on_event("Homed")
        self.robot.RegisterCallbacks(callbacks=self.callbacks, run_callbacks_in_separate_thread=True)

    def on_event(self, event):
        print(event)

    def connect(self):
        self.robot.Connect(address=self.address, disconnect_on_exception=False)

    def activate_and_home(self):
        self.robot.ActivateRobot()
        self.robot.Home()

    def set_trf(self, x, y, z, a, b, g):
        self.robot.SetTRF(x, y, z, a, b, g)

    def move_joints(self, joint1, joint2, joint3, joint4, joint5, joint6):
        self.robot.MoveJoints(joint1, joint2, joint3, joint4, joint5, joint6)

    def move_lin(self, x, y, z, a, b, g):
        self.robot.MoveLin(x, y, z, a, b, g)

    def move_lin_trf(self, x, y, z, a, b, g):
        self.robot.MoveLinRelTrf(x, y, z, a, b, g)

    def get_pose(self):
        return self.robot.GetPose()

    def get_joints(self):
        return self.robot.GetJoints()

    def set_joint_vel(self, speed):
        self.robot.SetJointVel(speed)

    def wait_idle(self):
        self.robot.WaitIdle()

    def deactivate_and_disconnect(self):
        self.robot.DeactivateRobot()
        self.robot.Disconnect()
