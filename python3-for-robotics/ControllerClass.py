import math


class Controller:
    ANGLE_THRESHOLD = math.radians(5.0)   # 5 degrees

    def __init__(self, forward_speed_gain, rotational_speed_gain):
        self._kv = forward_speed_gain
        self._kw = rotational_speed_gain

    @staticmethod
    def wrap_angle(angle):
        """Wrap an angle to the interval [-pi, pi]."""
        return math.atan2(math.sin(angle), math.cos(angle))

    @staticmethod
    def distance_to_target(actual_pos, target_pos):
        dx = target_pos[0] - actual_pos[0]
        dy = target_pos[1] - actual_pos[1]
        return math.hypot(dx, dy)

    def angle_error(self, actual_pos, target_pos):
        dx = target_pos[0] - actual_pos[0]
        dy = target_pos[1] - actual_pos[1]
        desired_theta = math.atan2(dy, dx)
        return self.wrap_angle(desired_theta - actual_pos[2])

    def compute_speeds(self, actual_pos, target_pos):
        """Return (forward_speed, rotational_speed) from the P controller."""
        e_theta = self.angle_error(actual_pos, target_pos)
        distance = self.distance_to_target(actual_pos, target_pos)

        omega = self._kw * e_theta

        if abs(e_theta) < self.ANGLE_THRESHOLD:
            vf = self._kv * distance
        else:
            vf = 0.0   # rotate in place until aligned

        return vf, omega