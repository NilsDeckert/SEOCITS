import math
import pybullet as p

class OrientationSensor:
    def __init__(self, robot_id):
        """
        Initialize the orientation sensor for a specific robot.
        
        :param robot_id: The PyBullet unique ID of the robot.
        """
        self.robot_id = robot_id

    def read(self):
        """
        Returns the [roll, pitch, yaw] orientation of the robot in radians.
        """
        _, orn = p.getBasePositionAndOrientation(self.robot_id)
        return list(p.getEulerFromQuaternion(orn))

    def get_heading_deg(self):
        """
        Returns the current heading of the robot in degrees
        """
        return math.degrees(self.read()[2])
