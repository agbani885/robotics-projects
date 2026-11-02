import math


class Robot:
    def __init__(self, name, max_speed=(0.3, 0.3), initial_pos=(0.0, 0.0, 0.0)):
        self._name = name
        self._max_linear, self._max_angular = max_speed
        self._x, self._y, self._theta = initial_pos
        self._vf = 0.0
        self._omega = 0.0
        self._t_k = None

    # --- name ---
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # --- pose ---
    def get_position(self):
        return (self._x, self._y, self._theta)

    # --- speeds (clamped to the maximum) ---
    def set_speeds(self, vf, omega):
        self._vf = max(0.0, min(vf, self._max_linear))
        self._omega = max(-self._max_angular, min(omega, self._max_angular))

    def get_speeds(self):
        return (self._vf, self._omega)

    # --- time / update ---
    def init_task(self, t_k):
        self._t_k = t_k

    def update(self, current_time):
        dt = current_time - self._t_k
        self._theta += self._omega * dt
        self._theta = math.atan2(math.sin(self._theta), math.cos(self._theta))
        self._x += self._vf * math.cos(self._theta) * dt
        self._y += self._vf * math.sin(self._theta) * dt
        self._t_k = current_time