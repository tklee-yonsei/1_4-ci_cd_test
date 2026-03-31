"""
MIMO 채널 시뮬레이션 모듈

Rayleigh fading 채널 모델을 기반으로 MIMO 시스템의 채널 용량을 계산합니다.
Shannon 용량 공식을 사용하여 다중 안테나 시스템의 이론적 최대 전송률을 추정합니다.
"""

import numpy as np


def generate_rayleigh_channel(n_rx, n_tx):
    """Rayleigh fading MIMO 채널 행렬을 생성합니다.

    각 원소는 독립적인 복소 가우시안 분포 CN(0, 1)를 따릅니다.
    실수부와 허수부 각각 N(0, 0.5)이므로 전체 분산은 1입니다.

    Parameters
    ----------
    n_rx : int
        수신 안테나 수
    n_tx : int
        송신 안테나 수

    Returns
    -------
    numpy.ndarray, shape (n_rx, n_tx), dtype complex128
        복소 채널 행렬 H
    """
    return (np.random.randn(n_rx, n_tx) + 1j * np.random.randn(n_rx, n_tx)) / np.sqrt(2)


def channel_capacity(H, snr_db):
    """MIMO 채널의 Shannon 용량을 계산합니다 (bits/s/Hz).

    송신 전력을 모든 안테나에 균등하게 분배한다고 가정합니다 (no CSIT).
    수식: C = log2(det(I + (SNR/n_tx) * H @ H^H))

    Parameters
    ----------
    H : numpy.ndarray, shape (n_rx, n_tx), dtype complex
        MIMO 채널 행렬
    snr_db : float
        수신 신호 대 잡음비 (dB 단위)

    Returns
    -------
    float
        채널 용량 (bits/s/Hz)
    """
    n_rx, n_tx = H.shape
    snr = 10 ** (snr_db / 10)
    I = np.eye(n_rx)
    capacity = np.log2(np.linalg.det(I + (snr / n_tx) * H @ H.conj().T).real)
    return capacity


if __name__ == "__main__":
    n_rx, n_tx = 4, 4
    n_trials = 1000
    snr_range = np.arange(0, 31, 5)

    print("===== MIMO 채널 용량 몬테카를로 시뮬레이션 =====")
    print(f"안테나: {n_rx}×{n_tx}, 시행 횟수: {n_trials}\n")

    avg_capacities = []
    for snr in snr_range:
        caps = [
            channel_capacity(generate_rayleigh_channel(n_rx, n_tx), snr)
            for _ in range(n_trials)
        ]
        avg_cap = np.mean(caps)
        avg_capacities.append(avg_cap)
        print(f"SNR = {snr:2d} dB → Avg Capacity = {avg_cap:.2f} bits/s/Hz")

    print("\n--- SISO vs MIMO 비교 ---")
    for snr, mimo_cap in zip(snr_range, avg_capacities):
        siso_cap = np.log2(1 + 10 ** (snr / 10))
        print(
            f"SNR {snr:2d} dB: SISO = {siso_cap:.2f}, "
            f"MIMO 4×4 = {mimo_cap:.2f}, "
            f"이득 = {mimo_cap / siso_cap:.1f}배"
        )
