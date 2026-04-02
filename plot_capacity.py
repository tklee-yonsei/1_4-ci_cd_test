"""
MIMO 채널 용량 비교 그래프

다양한 안테나 구성(SISO, 2×2, 4×4, 8×8)에서의
Ergodic 채널 용량을 SNR에 따라 비교합니다.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from plot_config import apply_style, save_figure
from numpy_channel import generate_rayleigh_channel, channel_capacity


def parse_args():
    parser = argparse.ArgumentParser(description="MIMO 채널 용량 비교 그래프 생성")
    parser.add_argument(
        "--output",
        type=str,
        default="mimo_capacity",
        help="출력 파일 접두사 (기본값: mimo_capacity)",
    )
    parser.add_argument(
        "--n-trials", type=int, default=500, help="몬테카를로 시행 횟수 (기본값: 500)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    apply_style()

    snr_range = np.arange(0, 31)
    configs = [(1, 1, "SISO"), (2, 2, "2×2"), (4, 4, "4×4"), (8, 8, "8×8")]
    markers = ["o", "s", "^", "D"]

    fig, ax = plt.subplots()
    for (n_rx, n_tx, label), marker in zip(configs, markers):
        avg_caps = []
        for snr in snr_range:
            caps = [
                channel_capacity(generate_rayleigh_channel(n_rx, n_tx), snr)
                for _ in range(args.n_trials)
            ]
            avg_caps.append(np.mean(caps))
        ax.plot(snr_range, avg_caps, marker=marker, markevery=5, label=label)

    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("Ergodic Capacity (bits/s/Hz)")
    ax.set_title("MIMO Channel Capacity vs SNR")
    ax.legend(title="Antenna Config")

    save_figure(fig, args.output)
    print("완료!")
