import math


class UserInterface:
    DEFAULT_NAME = "Robo"
    DEFAULT_INITIAL_POS = (0.0, 0.0, 0.0)   # x [m], y [m], theta [deg]
    DEFAULT_TARGET = (0.5, 0.5)             # [m]
    DEFAULT_KV = 1.0
    DEFAULT_KW = 1.0

    # ---------- low-level helpers ----------
    @staticmethod
    def _ask_text(prompt, default):
        try:
            answer = input("{} [{}]: ".format(prompt, default)).strip()
        except EOFError:
            print()
            return default
        return answer if answer else default

    @staticmethod
    def _ask_float(prompt, default, positive=False):
        while True:
            try:
                answer = input("{} [{}]: ".format(prompt, default)).strip()
            except EOFError:
                print()
                return float(default)
            if not answer:
                return float(default)
            try:
                value = float(answer.replace(",", "."))
            except ValueError:
                print("  -> Please enter a number.")
                continue
            if not math.isfinite(value):
                print("  -> Please enter a finite number.")
                continue
            if positive and value <= 0.0:
                print("  -> The value must be greater than zero.")
                continue
            return value

    # ---------- questions ----------
    def get_robot_config(self):
        """Return (name, initial_pos) with initial_pos = (x, y, theta_rad)."""
        print("\n--- Robot configuration ---")
        name = self._ask_text("Robot name", self.DEFAULT_NAME)
        x = self._ask_float("Initial X [m]", self.DEFAULT_INITIAL_POS[0])
        y = self._ask_float("Initial Y [m]", self.DEFAULT_INITIAL_POS[1])
        theta_deg = self._ask_float("Initial heading [deg]", self.DEFAULT_INITIAL_POS[2])
        return name, (x, y, math.radians(theta_deg))

    def get_target(self):
        print("\n--- Target position ---")
        tx = self._ask_float("Target X [m]", self.DEFAULT_TARGET[0])
        ty = self._ask_float("Target Y [m]", self.DEFAULT_TARGET[1])
        return [tx, ty]

    def get_gains(self):
        print("\n--- Controller gains ---")
        kv = self._ask_float("Forward speed gain Kv", self.DEFAULT_KV, positive=True)
        kw = self._ask_float("Rotational speed gain Kw", self.DEFAULT_KW, positive=True)
        return kv, kw

    # ---------- output ----------
    def show_start(self, name, initial_pos, target):
        print("\n{} starts at ({:.3f}, {:.3f}, {:.1f} deg) and goes to ({:.3f}, {:.3f})."
              .format(name, initial_pos[0], initial_pos[1],
                      math.degrees(initial_pos[2]), target[0], target[1]))

    def show_arrival(self, name, final_pos, target, elapsed):
        error = math.hypot(target[0] - final_pos[0], target[1] - final_pos[1])
        print("{} arrived to the target!".format(name))
        print("  Final position : ({:.4f}, {:.4f}) m, heading {:.1f} deg"
              .format(final_pos[0], final_pos[1], math.degrees(final_pos[2])))
        print("  Final distance error : {:.2f} cm".format(error * 100.0))
        print("  Elapsed time   : {:.2f} s".format(elapsed))

    def show_timeout(self, name, max_time):
        print("{} did not reach the target within {:.0f} s. Stopping.".format(name, max_time))