from collections import abc
import simulation
import math
import pybullet as p
import time
from .sensors import RobotSensors

class SimpleRobot:
    """A simple API wrapper for controlling a robot in PyBullet."""
    def __init__(self, urdf_path, start_pos, start_orn, simulation):
        # Load the robot into the PyBullet simulation
        self.id = p.loadURDF(urdf_path, start_pos, start_orn)
        self.time_step = 1.0 / 240.0
        self.wheel_indices = []
        self.sim = simulation
        for i in range(p.getNumJoints(self.id)):
            info = p.getJointInfo(self.id, i)
            joint_name = info[1].decode('utf-8')
            if "wheel" in joint_name:
                self.wheel_indices.append(i)
            if joint_name == "gripper_extension":
                p.resetJointState(self.id, i, targetValue=-0.38)
                p.setJointMotorControl2(self.id, i, p.POSITION_CONTROL, targetPosition=-0.38)

        self.sensors = RobotSensors(self.id)
                
    def _turn_off_motors(self):
        p.setJointMotorControlArray(
            bodyUniqueId=self.id,
            jointIndices=self.wheel_indices,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[0] * len(self.wheel_indices),
            forces=[10] * len(self.wheel_indices)
        )

    def _post_move(self):
        self._turn_off_motors()
        self.sim.sleep(0.5)
        # Update image in GUI
        self.sensors.get_rgb_image()
        # self.sensors.visualize_lidar()

    def _get_direction_facing(self):
        return self.sensors.get_direction_facing()

    def _get_position(self):
        return self.sensors.get_position()

    def show_camera_image(self):
        self.sensors.show_image()
    
    def get_rgb_image(self):
        return self.sensors.get_rgb_image()

    def get_base64_image(self):
        return self.sensors.get_base64_image()

    def get_lidar_scan(self):
        return self.sensors.get_lidar_scan()

    def visualize_lidar(self):
        self.sensors.visualize_lidar()
        
    def move_forward(self, distance):
        """
        Moves the robot forward by 'distance' units in the direction it is facing.
        This is a 'blocking' function: it steps the simulation itself 
        until the movement is complete.
        """
        target_velocity = 15  # Radians per second
        force = 10           # Maximum force to apply

        # Apply velocity control to all wheels simultaneously
        p.setJointMotorControlArray(
            bodyUniqueId=self.id,
            jointIndices=self.wheel_indices,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[-target_velocity] * len(self.wheel_indices),
            forces=[force] * len(self.wheel_indices)
        )

        # Run the simulation for a bit to move the robot
        self.sim.sleep(distance * 2)
        self._post_move()

    def turn(self, angle_degrees):
        """
        Turns the robot by a specific angle (in degrees).
        Positive angle turns counter-clockwise, negative turns clockwise.
        This is a 'blocking' function.
        """
        target_velocity = 15  # Radians per second
        force = 10           # Maximum force to apply

        if angle_degrees > 0:
            velocity_mask = [-1, -1, 1, 1]
        else:
            velocity_mask = [1, 1, -1, -1]

        target_angle = (self.sensors.get_direction_facing() + angle_degrees) % 360
        deviation = round(target_angle - self.sensors.get_direction_facing(), 1)

        # Apply velocity control to all wheels simultaneously
        p.setJointMotorControlArray(
            bodyUniqueId=self.id,
            jointIndices=self.wheel_indices,
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[target_velocity * v for v in velocity_mask],
            forces=[force] * len(self.wheel_indices)
        )

        while abs(deviation) > 1:
            p.stepSimulation()
            time.sleep(self.time_step)
            deviation = target_angle - self.sensors.get_direction_facing()
            deviation = deviation % 360

            if abs(deviation) < 5:
                # Slow down if close
                p.setJointMotorControlArray(
                    bodyUniqueId=self.id,
                    jointIndices=self.wheel_indices,
                    controlMode=p.VELOCITY_CONTROL,
                    targetVelocities=[target_velocity * 0.125 * v for v in velocity_mask],
                    forces=[force] * len(self.wheel_indices)
                )

        self._post_move()

    def turn_left(self, degrees: int):
        """
        Turn left by a given number of degrees.
        """
        self.turn(degrees)

    def turn_right(self, degrees: int):
        self.turn(-degrees)
