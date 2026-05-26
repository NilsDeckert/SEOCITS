import pybullet as p
import pybullet_data
import time
from .object import Object
from robot import SimpleRobot
from .recording import Recording

class Simulation:
    """
    This class is a helper to keep track of objects and their state inside the simulation.
    It also provides a utility function to progress the simulation forwards in time.
    """

    red = [1, 0, 0, 1]
    blue = [0, 0, 1, 1]
    green = [0, 1, 0, 1]
    yellow = [1, 1, 0, 1]
    purple = [1, 0, 1, 1]
    cyan = [0, 1, 1, 1]

    """Wraps the PyBullet environment setup."""
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        self.planeId = p.loadURDF("plane.urdf")
        self.bodies = []
        self._set_camera()

    def _set_camera(self):
        # Configure the camera for a top-down view
        p.resetDebugVisualizerCamera(
            cameraDistance=10,           # Distance from the target (height)
            cameraYaw=0,                 # Heading angle (0 degrees points North)
            cameraPitch=-89.9,           # Tilt angle (-90 is straight down)
            cameraTargetPosition=[0,0,0] # The point the camera is looking at
        )

    def new_recording(self, output_dir):
        self.recording = Recording(output_dir)
        self.recording.start()

    def sleep(self, seconds):
        """Idle the simulation for a set amount of time without freezing the GUI."""
        steps = int(seconds * 240)
        for _ in range(steps):
            p.stepSimulation()
            time.sleep(1.0 / 240.0)
            
    def disconnect(self):
        """
        Exit
        """
        if self.recording:
            self.recording.stop()
        p.disconnect()

    def reset_objects(self):
        """
        Reset objects to their initial position
        """
        for obj in self.bodies:
            p.resetBasePositionAndOrientation(obj.id, obj.pos, [0, 0, 0, 1])

    def spawn_cube_at(self, position, color=red):
        half_extents = [0.5, 0.5, 1]

        # 1. Physical properties
        col_box_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)
        # 2. Appearance
        vis_box_id = p.createVisualShape(p.GEOM_BOX, halfExtents=half_extents, rgbaColor=color)
        # 3. Create the body
        box_id = p.createMultiBody(
            baseMass=1.0,  # 0 makes it static (unmovable)
            baseCollisionShapeIndex=col_box_id,
            baseVisualShapeIndex=vis_box_id,
            basePosition=position
        )

        self.bodies.append(
            Object(
                id=box_id,
                pos=position,
                halfExtents=half_extents,
                color=color,
                shape="cube"
            )
        )

    def get_bodies(self, robot: SimpleRobot) -> str:
        """Return the description of all objects in the simulation as a string."""
        
        out = ""
        for obj in self.bodies:
            out += "- " + obj.get_description() + "\n"
            out += "  " + obj.get_relative_pos(robot) + "\n"

        return out
        
