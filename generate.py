"""
시뮬레이션 데이터 생성 모듈

Rayleigh fading 채널과 3GPP 경로 손실 모델을 기반으로
다양한 주파수 대역 및 시나리오의 시뮬레이션 데이터를 생성하고
HDF5 형식으로 저장합니다.
"""

import numpy as np
import h5py
import time
import os


def generate_scenario(n_samples, n_rx=4, n_tx=4, freq=3.5e9):
    """단일 시나리오의 시뮬레이션 데이터를 생성합니다.

    Parameters
    ----------
    n_samples : int
        생성할 채널 샘플 수
    n_rx : int
        수신 안테나 수 (기본값: 4)
    n_tx : int
        송신 안테나 수 (기본값: 4)
    freq : float
        반송파 주파수 Hz (기본값: 3.5e9)

    Returns
    -------
    dict
        channel_matrix, path_loss, distances 키를 가진 딕셔너리
    """
    H = (
        np.random.randn(n_samples, n_rx, n_tx)
        + 1j * np.random.randn(n_samples, n_rx, n_tx)
    ) / np.sqrt(2)
    distances = np.random.uniform(10, 500, n_samples)
    path_loss = 32.4 + 20 * np.log10(freq / 1e9) + 30 * np.log10(distances)
    return {
        "channel_matrix": H,
        "path_loss": path_loss,
        "distances": distances,
    }


def save_to_hdf5(filename, scenarios_data, frequencies):
    """시뮬레이션 결과를 HDF5 파일로 저장합니다.

    Parameters
    ----------
    filename : str
        저장할 HDF5 파일 경로
    scenarios_data : dict
        {freq: [scenario_dict, ...], ...} 구조의 데이터
    frequencies : list of float
        사용된 주파수 목록 (Hz)

    Returns
    -------
    None
    """
    with h5py.File(filename, "w") as f:
        f.attrs["created_by"] = "generate.py"
        f.attrs["n_frequencies"] = len(frequencies)

        for freq, scenarios in scenarios_data.items():
            freq_name = f"freq_{freq/1e9:.0f}GHz"
            freq_group = f.create_group(freq_name)
            freq_group.attrs["frequency_hz"] = freq

            for i, data in enumerate(scenarios):
                grp = freq_group.create_group(f"scenario_{i:03d}")
                grp.create_dataset(
                    "channel_matrix", data=data["channel_matrix"], compression="gzip"
                )
                grp.create_dataset("path_loss", data=data["path_loss"])
                grp.create_dataset("distances", data=data["distances"])


if __name__ == "__main__":
    print("===== 시뮬레이션 데이터 생성 =====")
    start = time.time()

    n_scenarios = 50
    n_samples = 200
    frequencies = [3.5e9, 28e9, 60e9]

    scenarios_data = {}
    for freq in frequencies:
        scenarios_data[freq] = [
            generate_scenario(n_samples, freq=freq) for _ in range(n_scenarios)
        ]

    save_to_hdf5("simulation.h5", scenarios_data, frequencies)

    elapsed = time.time() - start
    file_size = os.path.getsize("simulation.h5") / 1024 / 1024
    print(f"시나리오: {n_scenarios * len(frequencies)}개")
    print(f"파일 크기: {file_size:.1f} MB")
    print(f"소요 시간: {elapsed:.1f}초")
