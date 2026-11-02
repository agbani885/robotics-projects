import math
import os


def plot_results(history, target_pos, robot_name, show=False, filename="results.png"):
    """Save (and optionally show) the simulation plots. Never raises."""
    if len(history) < 2:
        print("Not enough data to plot.")
        return

    try:
        import matplotlib
        if not show:
            matplotlib.use("Agg")      # no window needed
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib is not installed: skipping plots (pip install matplotlib).")
        return

    t = [row[0] for row in history]
    x = [row[1] for row in history]
    y = [row[2] for row in history]
    theta = [row[3] for row in history]
    vf = [row[4] for row in history]
    omega = [row[5] for row in history]
    dist_cm = [row[6] * 100.0 for row in history]
    e_theta_deg = [math.degrees(row[7]) for row in history]

    fig, axs = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("Go-To-Target simulation - {}".format(robot_name))

    # 1) Trajectory
    ax = axs[0][0]
    ax.plot(x, y, color="tab:blue", label="Trajectory")
    step = max(1, len(x) // 15)
    ax.quiver(x[::step], y[::step],
              [math.cos(a) for a in theta[::step]],
              [math.sin(a) for a in theta[::step]],
              angles="xy", scale_units="xy", scale=8, width=0.004,
              color="tab:gray", label="Heading")
    ax.plot(x[0], y[0], "go", markersize=9, label="Start")
    ax.plot(target_pos[0], target_pos[1], "r*", markersize=14, label="Target")
    ax.add_patch(plt.Circle((target_pos[0], target_pos[1]), 0.01,
                            fill=False, color="red", linestyle="--"))
    ax.set_xlabel("X [m]")
    ax.set_ylabel("Y [m]")
    ax.set_title("Trajectory")
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(True)
    ax.legend(loc="best", fontsize=8)

    # 2) Forward speed
    ax = axs[0][1]
    ax.plot(t, vf, color="tab:green")
    ax.axhline(0.3, color="k", linestyle=":", label="Max 0.3 m/s")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Forward speed Vf [m/s]")
    ax.set_title("Forward speed")
    ax.grid(True)
    ax.legend(loc="best", fontsize=8)

    # 3) Rotational speed
    ax = axs[1][0]
    ax.plot(t, omega, color="tab:orange")
    ax.axhline(0.3, color="k", linestyle=":", label="Max +/-0.3 rad/s")
    ax.axhline(-0.3, color="k", linestyle=":")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Rotational speed w [rad/s]")
    ax.set_title("Rotational speed")
    ax.grid(True)
    ax.legend(loc="best", fontsize=8)

    # 4) Errors (two y axes)
    ax = axs[1][1]
    ax.plot(t, dist_cm, color="tab:red", label="Distance error [cm]")
    ax.axhline(1.0, color="tab:red", linestyle=":", label="1 cm tolerance")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Distance error [cm]", color="tab:red")
    ax.set_title("Errors")
    ax.grid(True)
    ax2 = ax.twinx()
    ax2.plot(t, e_theta_deg, color="tab:purple", label="Angle error [deg]")
    ax2.axhline(5.0, color="tab:purple", linestyle=":", label="+/-5 deg threshold")
    ax2.axhline(-5.0, color="tab:purple", linestyle=":")
    ax2.set_ylabel("Angle error [deg]", color="tab:purple")
    lines = ax.get_legend_handles_labels()
    lines2 = ax2.get_legend_handles_labels()
    ax.legend(lines[0] + lines2[0], lines[1] + lines2[1], loc="upper right", fontsize=8)

    fig.tight_layout()

    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        fig.savefig(path, dpi=150)
        print("Plots saved to: {}".format(path))
    except OSError as exc:
        print("Could not save the plots: {}".format(exc))

    if show:
        plt.show()
    plt.close(fig)