import config
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

    def _calc_corners(self):
        corners = []
        for i in range(4):
            # Cycle between -1 and 1.
            dx, dy = divmod(i, 2)
            dx = dx * 2 - 1
            dy = dy * 2 - 1
            
            hEx, hEy = self.halfExtents[:2]
            cx = self.pos[0] + dx * hEx
            cy = self.pos[1] + dy * hEy
                
            corners.append([cx, cy, 0])
        return corners

    def get_relative_pos(self, robot: SimpleRobot) -> str:
        """
        Return a natural language description of the angle and distance
        of this object in relation to the robot.

        NOTE: IN THIS CASE, THE ANGLES ARE IN THE WRONG DIRECTION DELIBERATELY
        """
        robot_pos = robot._get_position()
        robot_dir = robot._get_direction_facing(config.use_degrees)

        # Get coordinates of the objects corners
        corners = self._calc_corners()
        corner_distances = []
        corner_angles = []

        for corner in corners:
            distance = math.sqrt((corner[0] - robot_pos[0])**2 + (corner[1] - robot_pos[1])**2)
            distance = round(distance, 2)
            corner_distances.append(distance)
            angle = math.atan2(corner[1] - robot_pos[1], corner[0] - robot_pos[0])
            if config.use_degrees:
                angle = math.degrees(angle)
                angle = (angle - robot_dir) % 360
            else:
                angle = (angle - robot_dir) % (2 * math.pi)
            angle = round(angle, 2)
            if config.use_degrees:
                corner_angles.append(-angle)
            else:
                corner_angles.append(angle)

        out = ""
        for i in range(len(corners)):
            out += f"Corner {i+1}: {corner_distances[i]} meters away at {corner_angles[i]} {config.unit_angle}.\n"
        return out


    def get_description(self) -> str:
        obj = self.shape if self.shape else "object"
        width = round(self.halfExtents[0] * 2, 2)
        length = round(self.halfExtents[1] * 2, 2)
        height = round(self.halfExtents[2] * 2, 2)
        color = f"rgba({self.color[0]}, {self.color[1]}, {self.color[2]}, {self.color[3]})" if self.color else ""
        return f"{color} {obj} of width {width}, height {height} and length {length}."