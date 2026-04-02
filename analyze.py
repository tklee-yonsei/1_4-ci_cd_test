"""
시뮬레이션 데이터 분석 모듈

HDF5 파일에 저장된 시뮬레이션 결과를 읽어서
주파수별 경로 손실, 채널 용량 분포, CDF 그래프를 생성합니다.
"""

import argparse
import numpy as np
import h5py
import matplotlib.pyplot as plt
from plot_config import apply_style, save_figure, create_subplots


def load_and_analyze(filepath, snr_db=20):
    """HDF5 파일을 읽어서 주파수별 분석 데이터를 반환합니다.

    Parameters
    ----------
    filepath : str
        HDF5 파일 경로
    snr_db : float
        채널 용량 계산에 사용할 SNR (dB)

    Returns
    -------
    dict
        {freq_name: {path_loss, distances, capacity}, ...}
    """
    freq_data = {}
    with h5py.File(filepath, "r") as f:
        for freq_name in f.keys():
            all_pl, all_dist, all_capacity = [], [], []

            for sc_name in f[freq_name].keys():
                sc = f[f"{freq_name}/{sc_name}"]
                all_pl.extend(sc["path_loss"][:])
                all_dist.extend(sc["distances"][:])

                snr = 10 ** (snr_db / 10)
                for H in sc["channel_matrix"][:]:
                    I = np.eye(H.shape[0])
                    n_tx = H.shape[1]
                    cap = np.log2(np.linalg.det(I + (snr / n_tx) * H @ H.conj().T).real)
                    all_capacity.append(cap)

            freq_data[freq_name] = {
                "path_loss": np.array(all_pl),
                "distances": np.array(all_dist),
                "capacity": np.array(all_capacity),
            }
    return freq_data


def plot_analysis(freq_data, output_prefix):
    """분석 결과를 3개 서브플롯으로 시각화합니다.

    Parameters
    ----------
    freq_data : dict
        load_and_analyze()의 반환값
    output_prefix : str
        출력 파일 경로 (확장자 제외)
    """
    apply_style()
    fig, axes = create_subplots(3, fig_width_per_col=6, height=5)
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    # 그래프 1: Path Loss vs Distance
    for (name, data), color in zip(freq_data.items(), colors):
        label = name.replace("_", " ")
        axes[0].scatter(
            data["distances"], data["path_loss"], alpha=0.1, s=3, color=color
        )
        bins = np.linspace(10, 500, 20)
        bin_idx = np.digitize(data["distances"], bins)
        bin_means = [
            np.mean(data["path_loss"][bin_idx == j])
            for j in range(1, len(bins))
            if np.sum(bin_idx == j) > 0
        ]
        bin_centers = [
            (bins[j - 1] + bins[j]) / 2
            for j in range(1, len(bins))
            if np.sum(bin_idx == j) > 0
        ]
        axes[0].plot(
            bin_centers, bin_means, "o-", color=color, markersize=4, label=label
        )
    axes[0].set_xlabel("Distance (m)")
    axes[0].set_ylabel("Path Loss (dB)")
    axes[0].set_title("Path Loss vs Distance")
    axes[0].legend()

    # 그래프 2: 채널 용량 분포
    for (name, data), color in zip(freq_data.items(), colors):
        axes[1].hist(
            data["capacity"],
            bins=40,
            alpha=0.5,
            color=color,
            label=name.replace("_", " "),
            density=True,
        )
    axes[1].set_xlabel("Channel Capacity (bits/s/Hz)")
    axes[1].set_ylabel("Density")
    axes[1].set_title("Capacity Distribution")
    axes[1].legend()

    # 그래프 3: CDF
    for (name, data), color in zip(freq_data.items(), colors):
        sorted_cap = np.sort(data["capacity"])
        cdf = np.arange(1, len(sorted_cap) + 1) / len(sorted_cap)
        axes[2].plot(sorted_cap, cdf, color=color, label=name.replace("_", " "))
    axes[2].set_xlabel("Channel Capacity (bits/s/Hz)")
    axes[2].set_ylabel("CDF")
    axes[2].set_title("Capacity CDF")
    axes[2].legend()

    save_figure(fig, output_prefix)


def parse_args():
    """명령줄 인자를 파싱합니다."""
    parser = argparse.ArgumentParser(description="시뮬레이션 데이터 분석 및 시각화")
    parser.add_argument(
        "--input",
        type=str,
        default="simulation.h5",
        help="입력 HDF5 파일 (기본값: simulation.h5)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="analysis_result",
        help="출력 파일 접두사 (기본값: analysis_result)",
    )
    parser.add_argument(
        "--snr", type=float, default=20, help="채널 용량 계산 SNR (dB, 기본값: 20)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("===== 데이터 분석 시작 =====")
    print(f"입력: {args.input}")
    print(f"출력: {args.output}")
    print(f"SNR: {args.snr} dB")
    print()

    freq_data = load_and_analyze(args.input, snr_db=args.snr)

    for name, data in freq_data.items():
        print(
            f"  {name}: {len(data['path_loss'])} 샘플, "
            f"평균 PL = {np.mean(data['path_loss']):.1f} dB, "
            f"평균 용량 = {np.mean(data['capacity']):.1f} bits/s/Hz"
        )

    plot_analysis(freq_data, args.output)
    print("\n분석 완료!")
