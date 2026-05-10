from .position_sensor import PositionSensor
from .orientation_sensor import OrientationSensor
from .velocity_sensor import VelocitySensor
from .lidar_sensor import LidarSensor
from .camera import Camera

class RobotSensors:
    def __init__(self, robot_id):
        self.position = PositionSensor(robot_id)
        self.orientation = OrientationSensor(robot_id)
        self.velocity = VelocitySensor(robot_id)
        self.lidar = LidarSensor(robot_id)
        self.camera = Camera(robot_id)

    def get_position(self):
        return self.position.read()

    def get_orientation_euler(self):
        return self.orientation.read()

    def get_direction_facing(self):
        return self.orientation.get_heading_deg()

    def get_velocity(self):
        return self.velocity.read()

    def get_lidar_scan(self, num_rays=16, ray_length=5.0):
        return self.lidar.read(num_rays, ray_length)

    def visualize_lidar(self):
        rays = self.get_lidar_scan(num_rays=8)
        f = [f"{x:.1f}" for x in rays]#
        grid = [
            [f[1], f[0], f[7]],
            [f[2], "   ", f[6]],
            [f[3], f[4], f[5]]
        ]
        
        for row in grid:
            print(f"{row[0]:>5} {row[1]:>5} {row[2]:>5}")
        print("\n")

    def get_distance_ahead(self):
        return self.lidar.get_distance_ahead()

    def get_rgb_image(self):
        """
        Return numpy array of image.
        This also shows the image in the GUI
        """
        return self.camera.get_rgb_image()
