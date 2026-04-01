"""numpy_channel.py 유닛 테스트"""

import numpy as np
import pytest
from numpy_channel import generate_rayleigh_channel, channel_capacity


# ===== Fixture =====


@pytest.fixture
def channel_4x4():
    """재현 가능한 4×4 채널 행렬"""
    np.random.seed(42)
    return generate_rayleigh_channel(4, 4)


# ===== generate_rayleigh_channel 테스트 =====


class TestGenerateRayleighChannel:
    """Rayleigh 채널 생성 함수 테스트"""

    def test_shape(self):
        """출력 행렬의 형태가 (n_rx, n_tx)인지 확인"""
        H = generate_rayleigh_channel(4, 4)
        assert H.shape == (4, 4)

    def test_dtype(self):
        """출력이 복소수인지 확인"""
        H = generate_rayleigh_channel(4, 4)
        assert H.dtype == np.complex128

    @pytest.mark.parametrize(
        "n_rx, n_tx",
        [(1, 1), (2, 2), (4, 4), (8, 8), (4, 2), (2, 8)],
    )
    def test_various_shapes(self, n_rx, n_tx):
        """다양한 안테나 구성에서 형태가 올바른지 확인"""
        H = generate_rayleigh_channel(n_rx, n_tx)
        assert H.shape == (n_rx, n_tx)

    def test_statistical_properties(self):
        """대량 생성 시 평균이 0에 가까운지 확인 (Rayleigh 특성)"""
        n_samples = 10000
        channels = [generate_rayleigh_channel(4, 4) for _ in range(n_samples)]
        mean_real = np.mean([H.real.mean() for H in channels])
        mean_imag = np.mean([H.imag.mean() for H in channels])
        assert abs(mean_real) < 0.05
        assert abs(mean_imag) < 0.05

    def test_unit_variance(self):
        """원소의 분산이 약 1인지 확인"""
        n_samples = 10000
        channels = [generate_rayleigh_channel(4, 4) for _ in range(n_samples)]
        all_elements = np.concatenate([H.flatten() for H in channels])
        variance = np.var(all_elements)
        assert variance == pytest.approx(1.0, abs=0.1)


# ===== channel_capacity 테스트 =====


class TestChannelCapacity:
    """채널 용량 계산 함수 테스트"""

    def test_siso_known_value(self):
        """SISO에서 알려진 공식과 비교: C = log2(1 + SNR)"""
        # SISO: H = [1] (단위 채널)
        H = np.array([[1.0 + 0j]])
        snr_db = 10
        expected = np.log2(1 + 10 ** (snr_db / 10))
        result = channel_capacity(H, snr_db)
        assert result == pytest.approx(expected, rel=0.01)

    def test_capacity_increases_with_snr(self, channel_4x4):
        """SNR이 증가하면 용량도 증가해야 함"""
        cap_low = channel_capacity(channel_4x4, 0)
        cap_high = channel_capacity(channel_4x4, 30)
        assert cap_high > cap_low

    def test_capacity_non_negative(self, channel_4x4):
        """용량은 항상 0 이상"""
        for snr in range(0, 31, 5):
            cap = channel_capacity(channel_4x4, snr)
            assert cap >= 0

    def test_mimo_gain(self):
        """MIMO 용량이 SISO보다 큰지 확인 (동일 SNR에서)"""
        snr_db = 20
        np.random.seed(42)

        siso_caps = [
            channel_capacity(generate_rayleigh_channel(1, 1), snr_db)
            for _ in range(100)
        ]
        mimo_caps = [
            channel_capacity(generate_rayleigh_channel(4, 4), snr_db)
            for _ in range(100)
        ]
        assert np.mean(mimo_caps) > np.mean(siso_caps)
