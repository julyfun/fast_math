import numpy as np
from itp_state import ItpState, arr
from matplotlib import pyplot as plt
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, filter=lambda r: r["extra"].get("name") in ["itp_state"])


def test3():
    x0 = arr(0)
    v0 = arr(5)
    v_max = arr(2)
    a_max = arr(8)
    j_max = arr(500)
    fps = 300.0
    itp_state = ItpState()
    itp_state.init(x0, v0, v_max, a_max, j_max, fps)

    # 2hz 振幅 1m 的正弦序列，时间间隔 1 / 30s，持续 2s
    t_samples = np.arange(0, 10, 1 / 60)
    freq = 0.5
    amp = 0.5
    x_samples = np.sin(2 * np.pi * freq * t_samples) * amp
    # v_samples = 2 * np.pi * freq * np.cos(2 * np.pi * freq * t_samples) * amp
    v_samples = np.zeros_like(x_samples)

    # v_samples = np.zeros_like(x_samples)
    last_itpltn_t = 0
    res = []
    t_vals = []
    for i, (x, v, t) in enumerate(zip(x_samples, v_samples, t_samples)):
        if i == 444:
            itp_state.init(x0=arr(5), v0=arr(0))
        # 插到 t
        points_needed = int((t - last_itpltn_t) * fps)
        res += itp_state.interpolate(
            arr(x), arr(v), points_needed, first_delta_t=(last_itpltn_t - t)
        )
        t_vals += [last_itpltn_t + i / fps for i in range(points_needed)]
        last_itpltn_t += points_needed / fps

    res = np.array(res)
    x_vals = np.array(res[:, 0])
    v_vals = np.array(res[:, 1])
    a_vals = np.array(res[:, 2])
    j_vals = np.array(res[:, 3])

    def plot_subplots(t, data, titles, y_labels, extra_data=None, extra_t=None):
        plt.figure(figsize=(12, 8))
        for i, (data_vals, title, y_label) in enumerate(zip(data, titles, y_labels)):
            plt.subplot(4, 1, i + 1)
            for j in range(data_vals.shape[1]):
                plt.plot(
                    t,
                    data_vals[:, j],
                    marker="o",
                    linestyle="-",
                    label=f"Dimension {j+1}",
                )
            if extra_data is not None and extra_t is not None and i < len(extra_data):
                plt.plot(
                    extra_t,
                    extra_data[i],
                    marker="x",
                    linestyle="--",
                    label="Sample Data",
                )
            plt.axhline(
                0, color="gray", linestyle="--", linewidth=0.5
            )  # 添加 y=0 的水平线
            plt.title(title)
            plt.xlabel("Time (s)")
            plt.ylabel(y_label)
            plt.legend()
            plt.grid(True)
        plt.tight_layout()
        plt.show()

    data = [x_vals, v_vals, a_vals, j_vals]
    titles = ["X Position", "Velocity", "Acceleration", "Jerk"]
    y_labels = ["X Position", "Velocity", "Acceleration", "Jerk"]
    extra_data = [x_samples, v_samples]
    extra_t = t_samples

    plot_subplots(t_vals, data, titles, y_labels, extra_data, extra_t)


test3()