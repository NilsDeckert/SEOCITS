import config
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
        _, raw_orientation = p.getBasePositionAndOrientation(self.robot_id)

        # Rotate 90 degrees so that the sensor points forward
        correction_quat = p.getQuaternionFromEuler([0, 0, math.pi/2])
        orn = p.multiplyTransforms([0,0,0], raw_orientation, [0,0,0], correction_quat)[1]
        return list(p.getEulerFromQuaternion(orn))

    def get_heading(self):
        """
        Return the robots current heading in the configured unit
        """
        if config.use_degrees:
            return self.get_heading_deg()
        return self.get_heading_rad()

    def get_heading_deg(self):
        """
        Returns the current heading of the robot in degrees
        """
        return math.degrees(self.read()[2])
    
    def get_heading_rad(self):
        """
        Returns the current heading of the robot
        """
        return self.read()[2]
