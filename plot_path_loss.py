import numpy as np
import matplotlib.pyplot as plt
from plot_config import apply_style, save_figure

apply_style()

distances = np.linspace(10, 1000, 200)

models = {
    "Free Space": lambda d: 32.4 + 20 * np.log10(3.5) + 20 * np.log10(d),
    "3GPP UMa LOS": lambda d: 28.0 + 22 * np.log10(d) + 20 * np.log10(3.5),
    "3GPP UMa NLOS": lambda d: 13.54 + 39.08 * np.log10(d) + 20 * np.log10(3.5),
}
styles = ["-", "--", "-."]

fig, ax = plt.subplots()
for (name, func), style in zip(models.items(), styles):
    ax.plot(distances, func(distances), style, label=name)

ax.set_xlabel("Distance (m)")
ax.set_ylabel("Path Loss (dB)")
ax.set_title("Path Loss Models at 3.5 GHz")
ax.legend()

save_figure(fig, "path_loss_models")
plt.show()
print("완료!")
