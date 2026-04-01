import numpy as np
import h5py
import time
import os

print("===== 시뮬레이션 데이터 생성 =====")
start = time.time()

n_scenarios = 50
n_samples = 200
frequencies = [3.5e9, 28e9, 60e9]

with h5py.File("simulation.h5", "w") as f:
    f.attrs["created_by"] = "generate.py"
    f.attrs["n_scenarios"] = n_scenarios

    for freq in frequencies:
        freq_name = f"freq_{freq/1e9:.0f}GHz"
        freq_group = f.create_group(freq_name)
        freq_group.attrs["frequency_hz"] = freq

        for i in range(n_scenarios):
            H = (
                np.random.randn(n_samples, 4, 4) + 1j * np.random.randn(n_samples, 4, 4)
            ) / np.sqrt(2)
            distances = np.random.uniform(10, 500, n_samples)
            path_loss = 32.4 + 20 * np.log10(freq / 1e9) + 30 * np.log10(distances)

            grp = freq_group.create_group(f"scenario_{i:03d}")
            grp.create_dataset("channel_matrix", data=H, compression="gzip")
            grp.create_dataset("path_loss", data=path_loss)
            grp.create_dataset("distances", data=distances)

elapsed = time.time() - start
file_size = os.path.getsize("simulation.h5") / 1024 / 1024
print(f"시나리오: {n_scenarios * len(frequencies)}개")
print(f"파일 크기: {file_size:.1f} MB")
print(f"소요 시간: {elapsed:.1f}초")
