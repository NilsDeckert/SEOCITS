import pybullet as p

class PositionSensor:
    def __init__(self, robot_id):
        """
        Initialize the position sensor for a specific robot.
        
        :param robot_id: The PyBullet unique ID of the robot.
        """
        self.robot_id = robot_id

    def read(self):
        """
        Returns the [x, y, z] position of the robot's base.
        """
        pos, _ = p.getBasePositionAndOrientation(self.robot_id)
        return list(pos)
