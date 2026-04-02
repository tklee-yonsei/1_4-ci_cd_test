"""CLI 인터페이스 테스트"""

import subprocess
import os
import pytest


class TestGenerateCLI:
    """generate.py CLI 테스트"""

    def test_help(self):
        """--help가 정상 동작하는지 확인"""
        result = subprocess.run(
            ["python", "generate.py", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "시뮬레이션" in result.stdout or "simulation" in result.stdout.lower()

    def test_generate_with_args(self, tmp_path):
        """파라미터를 전달하여 데이터 생성"""
        output = str(tmp_path / "test.h5")
        result = subprocess.run(
            [
                "python",
                "generate.py",
                "--n-scenarios",
                "2",
                "--n-samples",
                "10",
                "--frequencies",
                "3.5",
                "--output",
                output,
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert os.path.exists(output)


class TestAnalyzeCLI:
    """analyze.py CLI 테스트"""

    def test_help(self):
        """--help가 정상 동작하는지 확인"""
        result = subprocess.run(
            ["python", "analyze.py", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
