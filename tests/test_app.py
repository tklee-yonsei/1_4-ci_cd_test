"""Flask API 엔드포인트 테스트"""

import os
import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    """테스트용 Flask 클라이언트

    DATA_DIR을 임시 디렉토리로 설정하여 테스트 간 격리.
    """
    monkeypatch.setenv("DATA_DIR", str(tmp_path))

    # app을 지연 import하여 환경 변수를 반영
    import importlib
    import app as app_module

    importlib.reload(app_module)

    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c


class TestHealth:
    """헬스 체크"""

    def test_health_ok(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json == {"status": "ok"}


class TestGenerate:
    """generate API"""

    def test_generate_default(self, client):
        """기본 파라미터로 생성"""
        response = client.post(
            "/api/generate",
            json={"n_scenarios": 2, "n_samples": 10, "frequencies": [3.5]},
        )
        assert response.status_code == 200
        data = response.json
        assert data["status"] == "success"
        assert data["n_scenarios"] == 2
        assert "file_size_mb" in data

    def test_generate_multiple_frequencies(self, client):
        """여러 주파수로 생성"""
        response = client.post(
            "/api/generate",
            json={
                "n_scenarios": 3,
                "n_samples": 5,
                "frequencies": [3.5, 28],
            },
        )
        assert response.status_code == 200
        assert response.json["n_scenarios"] == 6  # 3 * 2


class TestAnalyze:
    """analyze API"""

    def test_analyze_requires_input(self, client):
        """입력 파일이 없으면 404"""
        response = client.post(
            "/api/analyze",
            json={"input": "nonexistent.h5"},
        )
        assert response.status_code == 404

    def test_generate_then_analyze(self, client):
        """생성 후 분석"""
        # 먼저 생성
        client.post(
            "/api/generate",
            json={"n_scenarios": 2, "n_samples": 10, "frequencies": [3.5]},
        )
        # 분석
        response = client.post(
            "/api/analyze",
            json={"input": "simulation.h5", "snr": 20},
        )
        assert response.status_code == 200
        data = response.json
        assert data["status"] == "success"
        assert "summary" in data
        assert data["output_png"] == "analysis_result.png"


class TestResults:
    """results API"""

    def test_list_empty(self, client):
        """빈 디렉토리"""
        response = client.get("/api/results")
        assert response.status_code == 200
        assert response.json == {"files": []}

    def test_list_after_generate(self, client):
        """생성 후 파일 목록 확인"""
        client.post(
            "/api/generate",
            json={"n_scenarios": 2, "n_samples": 10, "frequencies": [3.5]},
        )
        response = client.get("/api/results")
        files = response.json["files"]
        filenames = [f["name"] for f in files]
        assert "simulation.h5" in filenames
