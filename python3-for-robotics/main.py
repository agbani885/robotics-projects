import math
import time


from RobotClass import Robot
from  ControllerClass import Controller
from UserInterface import UserInterface
from plotter import plot_results

ITERATION_TIME_SEC = 0.001   # 1 ms, as required
POSITION_TOLERANCE = 0.01    # 1 cm, as required
MAX_SIM_TIME_SEC = 300.0     # safety timeout
MAX_SPEED = (0.3, 0.3)       # (m/s, rad/s)

SHOW_PLOTS = False   # True = also open a window (blocks until you close it)

def run_simulation(robot, controller, target_pos):
    """Run the go-to-target loop. Returns (history, arrived, elapsed)."""
    history = []   # rows: t, x, y, theta, vf, omega, distance_error, angle_error
    arrived = False

    t_start = time.perf_counter()
    robot.init_task(t_start)

    try:
        while True:
            actual_pos = robot.get_position()
            distance = controller.distance_to_target(actual_pos, target_pos)
            now = time.perf_counter()
            elapsed = now - t_start

            if distance < POSITION_TOLERANCE:
                arrived = True
                break
            if elapsed > MAX_SIM_TIME_SEC:
                break

            # Controller -> robot
            vf, omega = controller.compute_speeds(actual_pos, target_pos)
            robot.set_speeds(vf, omega)

            # Record what the robot is actually doing (after clamping)
            real_vf, real_omega = robot.get_speeds()
            e_theta = controller.angle_error(actual_pos, target_pos)
            history.append((elapsed, actual_pos[0], actual_pos[1], actual_pos[2],
                            real_vf, real_omega, distance, e_theta))

            # Wait one iteration, then advance the robot by the real elapsed time
            time.sleep(ITERATION_TIME_SEC)
            robot.update(time.perf_counter())

    except KeyboardInterrupt:
        print("\nInterrupted by the user.")

    # Stop the robot
    robot.set_speeds(0.0, 0.0)
    elapsed = time.perf_counter() - t_start
    return history, arrived, elapsed


def main():
    ui = UserInterface()

    name, initial_pos = ui.get_robot_config()
    target_pos = ui.get_target()
    kv, kw = ui.get_gains()

    robot = Robot(name, MAX_SPEED, initial_pos)
    controller = Controller(kv, kw)

    ui.show_start(name, initial_pos, target_pos)
    history, arrived, elapsed = run_simulation(robot, controller, target_pos)

    if arrived:
        ui.show_arrival(robot.get_name(), robot.get_position(), target_pos, elapsed)
    else:
        ui.show_timeout(robot.get_name(), MAX_SIM_TIME_SEC)

    plot_results(history, target_pos, robot.get_name(), show=SHOW_PLOTS)

    return history


if __name__ == "__main__":
    history = main()
    if SHOW_PLOTS:
        plot_results(history)