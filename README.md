# Robotics Projects

A collection of coursework projects in robotics and state estimation, written in Python.

| Folder | Topic |
|---|---|
| `bundle-adjustment/` | Bundle adjustment (Jupyter notebook) |
| `recursive-bayes-filter/` | Recursive Bayes filter (Jupyter notebook) |
| `icp/` | Iterative Closest Point (ICP) point-cloud alignment |
| `lie-algebra/` | Rotation distance and Lie algebra (SO(3)) |
| `mapping/` | Occupancy grid mapping |
| `particle-filters/` | Monte Carlo localization with a particle filter |
| `python3-for-robotics/` | Go-to-target robot simulation: robot model, controller, UI and plotting, with result plots for different gains |

## Requirements

Python 3, NumPy, SciPy, Matplotlib and OpenCV (`opencv-python`). Jupyter is needed to open the notebooks.

```bash
pip install numpy scipy matplotlib opencv-python jupyter
```

## Running

- Notebooks: `jupyter notebook`, then open the one you want.
- `python3-for-robotics`: `cd python3-for-robotics && python main.py`
