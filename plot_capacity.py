import numpy as np
import matplotlib.pyplot as plt
from plot_config import apply_style, save_figure
from numpy_channel import generate_rayleigh_channel, channel_capacity

apply_style()

snr_range = np.arange(0, 31)
n_trials = 500

configs = [(1, 1, "SISO"), (2, 2, "2×2"), (4, 4, "4×4"), (8, 8, "8×8")]
markers = ["o", "s", "^", "D"]

fig, ax = plt.subplots()
for (n_rx, n_tx, label), marker in zip(configs, markers):
    avg_caps = []
    for snr in snr_range:
        caps = [
            channel_capacity(generate_rayleigh_channel(n_rx, n_tx), snr)
            for _ in range(n_trials)
        ]
        avg_caps.append(np.mean(caps))
    ax.plot(snr_range, avg_caps, marker=marker, markevery=5, label=label)

ax.set_xlabel("SNR (dB)")
ax.set_ylabel("Ergodic Capacity (bits/s/Hz)")
ax.set_title("MIMO Channel Capacity vs SNR")
ax.legend(title="Antenna Config")

save_figure(fig, "mimo_capacity")
plt.show()
print("완료!")
