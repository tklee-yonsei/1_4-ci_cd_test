# Changelog

## [v1.5] - 2026-04-01

### Added
- CI/CD 파이프라인 구축 (GitHub Actions)
  - Black 포맷 검사 (lint job)
  - pytest 자동 실행 (test job, lint 통과 후 실행)
- 유닛 테스트 추가
  - `test_generate.py`: 시뮬레이션 데이터 생성 함수 테스트 (채널 행렬 shape/dtype, 경로 손실, 거리 범위 검증)
  - `test_numpy_channel.py`: Rayleigh 채널 및 채널 용량 계산 함수 테스트
- pytest 설정 (`pyproject.toml`)
- CI 배지를 README에 추가

### Changed
- `generate.py` 코드 리팩토링 (함수 분리 및 구조 개선)
- `requirements.txt`에 테스트 의존성 추가 (`pytest`, `numpy`, `h5py`)

## [v1.0]

- 초기 릴리즈
- Rayleigh fading 채널 시뮬레이션
- 3GPP 경로 손실 모델
- HDF5 데이터 저장
- 시각화 기능
