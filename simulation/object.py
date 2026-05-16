import math
from robot import SimpleRobot

class Object():
    """
    This class contains code store info about an object in the simulation.
    It is used to give the operator LLM information about the known environment.

    In real life, this info would have to be gathered first using sensor. In our case,
    we use this simplification to focus on the *use* of relative coordinates instead of
    their extraction.
    """
    def __init__(self,
     id: int,
     pos: tuple[int, int, int],
     halfExtents: tuple[float, float, float],
     color: tuple[float, float, float, float] = None,
     shape: str = None):
        self.id = id
        self.pos = pos
        self.halfExtents = halfExtents
        self.color = color
        self.shape = shape

    def get_relative_pos(self, robot: SimpleRobot) -> str:
        """
        Return a natural language description of the angle and distance
        of this object in relation to the robot.
        """
        robot_pos = robot._get_position()
        robot_dir = robot._get_direction_facing()

        distance = math.sqrt((self.pos[0] - robot_pos[0])**2 + (self.pos[1] - robot_pos[1])**2)
        distance = round(distance, 2)
        
        angle = math.atan2(self.pos[1] - robot_pos[1], self.pos[0] - robot_pos[0])

        # TODO: Check direction of the angle. Clockwise positive or negative?
        angle = math.degrees(angle)
        angle = (angle - robot_dir) % 360
        angle = round(angle, 2)
        return f"The object is {distance} units away at an angle of {angle} degrees."

    def get_description(self) -> str:
        obj = self.shape if self.shape else "object"
        width = round(self.halfExtents[0] * 2, 2)
        length = round(self.halfExtents[1] * 2, 2)
        height = round(self.halfExtents[2] * 2, 2)
        color = f"rgba({self.color[0]}, {self.color[1]}, {self.color[2]}, {self.color[3]})" if self.color else ""
        return f"{color} {obj} of width {width}, height {height} and length {length}."