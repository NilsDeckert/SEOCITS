import pybullet as p
import math

class LidarSensor:
    def __init__(self, robot_id):
        """
        Initialize the LiDAR sensor for a specific robot.
        
        :param robot_id: The PyBullet unique ID of the robot.
        """
        self.robot_id = robot_id

    def read(self, num_rays=16, ray_length=5.0):
        """
        Simulates a 2D LiDAR scan around the robot.
        
        :param num_rays: The number of rays to cast in a 360 degree circle.
        :param ray_length: The maximum distance the LiDAR can detect.
        :return: A list of distances for each ray. If no object is hit, the distance will be ray_length.
        """
        pos, orn = p.getBasePositionAndOrientation(self.robot_id)
        euler = p.getEulerFromQuaternion(orn)
        yaw = euler[2]

        ray_starts = []
        ray_ends = []
        
        # Start rays slightly above the base z-coordinate
        start_z = pos[2] + 0.1

        for i in range(num_rays):
            angle = yaw + (i * 2.0 * math.pi / num_rays)
            start = [pos[0], pos[1], start_z]
            end = [
                pos[0] + ray_length * math.cos(angle),
                pos[1] + ray_length * math.sin(angle),
                start_z
            ]
            ray_starts.append(start)
            ray_ends.append(end)

        results = p.rayTestBatch(ray_starts, ray_ends)
        
        distances = []
        for res in results:
            hit_fraction = res[2]
            distances.append(hit_fraction * ray_length)
            
        return distances
