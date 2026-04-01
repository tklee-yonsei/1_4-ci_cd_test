import numpy as np
import h5py
import matplotlib.pyplot as plt
from plot_config import apply_style, save_figure, create_subplots

apply_style()
print("===== 데이터 분석 시작 =====")

with h5py.File("simulation.h5", "r") as f:
    print(f"주파수 대역: {list(f.keys())}")

    freq_data = {}
    for freq_name in f.keys():
        all_pl, all_dist, all_capacity = [], [], []

        for sc_name in f[freq_name].keys():
            sc = f[f"{freq_name}/{sc_name}"]
            all_pl.extend(sc["path_loss"][:])
            all_dist.extend(sc["distances"][:])

            snr = 10 ** (20 / 10)
            for H in sc["channel_matrix"][:]:
                I = np.eye(4)
                cap = np.log2(np.linalg.det(I + (snr / 4) * H @ H.conj().T).real)
                all_capacity.append(cap)

        freq_data[freq_name] = {
            "path_loss": np.array(all_pl),
            "distances": np.array(all_dist),
            "capacity": np.array(all_capacity),
        }
        print(
            f"  {freq_name}: {len(all_pl)} 샘플, "
            f"평균 PL = {np.mean(all_pl):.1f} dB, "
            f"평균 용량 = {np.mean(all_capacity):.1f} bits/s/Hz"
        )

# 그래프 생성
fig, axes = create_subplots(3, fig_width_per_col=6, height=5)
colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

# 그래프 1: Path Loss vs Distance
for (name, data), color in zip(freq_data.items(), colors):
    label = name.replace("_", " ")
    axes[0].scatter(data["distances"], data["path_loss"], alpha=0.1, s=3, color=color)
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
    axes[0].plot(bin_centers, bin_means, "o-", color=color, markersize=4, label=label)
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
axes[1].set_title("Capacity Distribution (SNR=20dB)")
axes[1].legend()

# 그래프 3: CDF
for (name, data), color in zip(freq_data.items(), colors):
    sorted_cap = np.sort(data["capacity"])
    cdf = np.arange(1, len(sorted_cap) + 1) / len(sorted_cap)
    axes[2].plot(sorted_cap, cdf, color=color, label=name.replace("_", " "))
axes[2].set_xlabel("Channel Capacity (bits/s/Hz)")
axes[2].set_ylabel("CDF")
axes[2].set_title("Capacity CDF (SNR=20dB)")
axes[2].legend()

save_figure(fig, "analysis_result")
plt.show()
print("\n분석 완료!")
