"""
Path Loss 모델 비교 그래프

Free Space, 3GPP UMa LOS/NLOS 모델을 비교합니다.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from plot_config import apply_style, save_figure


def parse_args():
    parser = argparse.ArgumentParser(description="Path Loss 모델 비교 그래프 생성")
    parser.add_argument(
        "--output",
        type=str,
        default="path_loss_models",
        help="출력 파일 접두사 (기본값: path_loss_models)",
    )
    parser.add_argument(
        "--freq", type=float, default=3.5, help="주파수 (GHz, 기본값: 3.5)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    apply_style()

    distances = np.linspace(10, 1000, 200)
    f = args.freq

    models = {
        "Free Space": lambda d: 32.4 + 20 * np.log10(f) + 20 * np.log10(d),
        "3GPP UMa LOS": lambda d: 28.0 + 22 * np.log10(d) + 20 * np.log10(f),
        "3GPP UMa NLOS": lambda d: 13.54 + 39.08 * np.log10(d) + 20 * np.log10(f),
    }
    styles = ["-", "--", "-."]

    fig, ax = plt.subplots()
    for (name, func), style in zip(models.items(), styles):
        ax.plot(distances, func(distances), style, label=name)

    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Path Loss (dB)")
    ax.set_title(f"Path Loss Models at {f} GHz")
    ax.legend()

    save_figure(fig, args.output)
    print("완료!")
