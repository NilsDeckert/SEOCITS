import pybullet as p
import pybullet_data
import time

class Simulation:

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
        
    def sleep(self, seconds):
        """Idle the simulation for a set amount of time without freezing the GUI."""
        steps = int(seconds * 240)
        for _ in range(steps):
            p.stepSimulation()
            time.sleep(1.0 / 240.0)
            
    def disconnect(self):
        p.disconnect()

    def spawn_cube_at(self, position, color=red):
        # 1. Physical properties
        col_box_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 1])
        # 2. Appearance
        vis_box_id = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 0.5, 1], rgbaColor=color)
        # 3. Create the body
        box_id = p.createMultiBody(
            baseMass=1.0,  # 0 makes it static (unmovable)
            baseCollisionShapeIndex=col_box_id,
            baseVisualShapeIndex=vis_box_id,
            basePosition=position
        )
