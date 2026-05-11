import cv2
import pybullet as p
import numpy as np
import math
import base64

class Camera:
    def __init__(self, robot_id, width=320, height=320):
        self.robot_id = robot_id
        self.width = width
        self.height = height
        self.near = 0.1
        self.far = 10.0  # Adjust based on how far you want to "see"
        self.fov = 60
        
        # Precompute projection matrix
        self.proj_matrix = p.computeProjectionMatrixFOV(
            fov=self.fov, aspect=1.0, nearVal=self.near, farVal=self.far
        )

    def _get_view_matrix(self):
        """Calculates the view matrix based on current robot pose."""
        pos, orient = p.getBasePositionAndOrientation(self.robot_id)
        rot_mat = p.getMatrixFromQuaternion(orient)
        
        # Forward vector (X-axis of the robot)
        forward = [rot_mat[1], rot_mat[4], rot_mat[7]]
        # Up vector (Z-axis)
        up = [rot_mat[2], rot_mat[5], rot_mat[8]]
        
        eye = [pos[0] + 0.1 * forward[0], pos[1] + 0.1 * forward[1], pos[2] + 0.3]
        target = [pos[0] + 1.0 * forward[0], pos[1] + 1.0 * forward[1], pos[2] + 0.3]
        
        return p.computeViewMatrix(eye, target, up)

    def get_rgb_image(self):
        """Returns a standard RGB array."""
        _, _, rgb, _, _ = p.getCameraImage(
            self.width, self.height, self._get_view_matrix(), self.proj_matrix
        )
        # Convert to numpy and drop alpha channel
        return np.reshape(rgb, (self.height, self.width, 4)) * 1. / 255.

    def get_base64_image(self):
        """Returns a base64 encoded PNG of the camera view."""
        image = self.get_rgb_image()
        image_uint8 = (image * 255).astype(np.uint8)
        image_bgr = cv2.cvtColor(image_uint8, cv2.COLOR_RGBA2BGR)
        _, buffer = cv2.imencode('.png', image_bgr)
        return base64.b64encode(buffer).decode('utf-8')

    def show_image(self):
        image = self.get_rgb_image()
        cv2.imshow("Camera", image)
        cv2.waitKey(1)