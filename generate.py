"""
시뮬레이션 데이터 생성 모듈

Rayleigh fading 채널과 3GPP 경로 손실 모델을 기반으로
다양한 주파수 대역 및 시나리오의 시뮬레이션 데이터를 생성하고
HDF5 형식으로 저장합니다.
"""

import argparse
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
    # 출력 디렉토리 생성
    output_dir = os.path.dirname(filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

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


def parse_args():
    """명령줄 인자를 파싱합니다."""
    parser = argparse.ArgumentParser(description="통신 채널 시뮬레이션 데이터 생성")
    parser.add_argument(
        "--n-scenarios", type=int, default=50, help="주파수당 시나리오 수 (기본값: 50)"
    )
    parser.add_argument(
        "--n-samples", type=int, default=200, help="시나리오당 샘플 수 (기본값: 200)"
    )
    parser.add_argument(
        "--frequencies",
        type=float,
        nargs="+",
        default=[3.5, 28, 60],
        help="주파수 목록 (GHz 단위, 기본값: 3.5 28 60)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="simulation.h5",
        help="출력 파일 경로 (기본값: simulation.h5)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    frequencies = [f * 1e9 for f in args.frequencies]  # GHz → Hz 변환

    print("===== 시뮬레이션 데이터 생성 =====")
    print(f"시나리오 수: {args.n_scenarios}")
    print(f"샘플 수: {args.n_samples}")
    print(f"주파수: {args.frequencies} GHz")
    print(f"출력: {args.output}")
    print()

    start = time.time()

    scenarios_data = {}
    for freq in frequencies:
        scenarios_data[freq] = [
            generate_scenario(args.n_samples, freq=freq)
            for _ in range(args.n_scenarios)
        ]

    save_to_hdf5(args.output, scenarios_data, frequencies)

    elapsed = time.time() - start
    file_size = os.path.getsize(args.output) / 1024 / 1024
    print(f"시나리오: {args.n_scenarios * len(frequencies)}개")
    print(f"파일 크기: {file_size:.1f} MB")
    print(f"소요 시간: {elapsed:.1f}초")
