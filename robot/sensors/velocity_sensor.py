import pybullet as p

class VelocitySensor:
    def __init__(self, robot_id):
        """
        Initialize the velocity sensor for a specific robot.
        
        :param robot_id: The PyBullet unique ID of the robot.
        """
        self.robot_id = robot_id

    def read(self):
        """
        Returns the linear [x, y, z] and angular [wx, wy, wz] velocity of the robot.
        """
        linear, angular = p.getBaseVelocity(self.robot_id)
        return list(linear), list(angular)
