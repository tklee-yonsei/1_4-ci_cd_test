"""generate.py 유닛 테스트"""

import numpy as np
import h5py
import os
import pytest
from generate import generate_scenario, save_to_hdf5


class TestGenerateScenario:
    """시나리오 생성 함수 테스트"""

    def test_returns_dict(self):
        """반환값이 올바른 키를 가진 딕셔너리인지 확인"""
        result = generate_scenario(10)
        assert "channel_matrix" in result
        assert "path_loss" in result
        assert "distances" in result

    def test_channel_matrix_shape(self):
        """채널 행렬 형태 확인"""
        result = generate_scenario(64, n_rx=4, n_tx=4)
        assert result["channel_matrix"].shape == (64, 4, 4)

    def test_channel_matrix_complex(self):
        """채널 행렬이 복소수인지 확인"""
        result = generate_scenario(10)
        assert result["channel_matrix"].dtype == np.complex128

    def test_path_loss_shape(self):
        """경로 손실 배열 길이 확인"""
        result = generate_scenario(100)
        assert result["path_loss"].shape == (100,)

    def test_distances_range(self):
        """거리가 10~500m 범위인지 확인"""
        result = generate_scenario(1000)
        assert result["distances"].min() >= 10
        assert result["distances"].max() <= 500

    def test_path_loss_increases_with_distance(self):
        """먼 거리일수록 경로 손실이 큰지 확인 (통계적)"""
        result = generate_scenario(1000)
        near = result["path_loss"][result["distances"] < 100]
        far = result["path_loss"][result["distances"] > 400]
        assert np.mean(far) > np.mean(near)


class TestSaveToHdf5:
    """HDF5 저장 함수 테스트"""

    @pytest.fixture
    def hdf5_file(self, tmp_path):
        """임시 HDF5 파일 생성"""
        filepath = str(tmp_path / "test_sim.h5")
        frequencies = [3.5e9, 28e9]
        scenarios_data = {
            freq: [generate_scenario(10, freq=freq) for _ in range(3)]
            for freq in frequencies
        }
        save_to_hdf5(filepath, scenarios_data, frequencies)
        return filepath

    def test_file_created(self, hdf5_file):
        """파일이 생성되었는지 확인"""
        assert os.path.exists(hdf5_file)

    def test_frequency_groups(self, hdf5_file):
        """주파수별 그룹이 올바르게 생성되었는지 확인"""
        with h5py.File(hdf5_file, "r") as f:
            assert "freq_4GHz" in f or "freq_3GHz" in f or "freq_28GHz" in f
            assert len(f.keys()) == 2  # 2개 주파수

    def test_scenario_count(self, hdf5_file):
        """시나리오 수가 올바른지 확인"""
        with h5py.File(hdf5_file, "r") as f:
            for freq_name in f.keys():
                assert len(f[freq_name].keys()) == 3  # 3개 시나리오

    def test_datasets_exist(self, hdf5_file):
        """각 시나리오에 필요한 데이터셋이 있는지 확인"""
        with h5py.File(hdf5_file, "r") as f:
            for freq_name in f.keys():
                for sc_name in f[freq_name].keys():
                    sc = f[f"{freq_name}/{sc_name}"]
                    assert "channel_matrix" in sc
                    assert "path_loss" in sc
                    assert "distances" in sc

    def test_metadata(self, hdf5_file):
        """메타데이터가 올바르게 저장되었는지 확인"""
        with h5py.File(hdf5_file, "r") as f:
            assert f.attrs["created_by"] == "generate.py"
