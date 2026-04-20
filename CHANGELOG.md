# Changelog

## [v2.1] - 2026-04-20

### [v2.1] - Added
- Flask API 서버 (app.py)
  - GET /api/health
  - POST /api/generate
  - POST /api/analyze
  - GET /api/results
  - GET /api/results/<filename>
- 웹 UI (templates/index.html)
- docker-compose.yml에 web 서비스 추가
- API 엔드포인트 테스트 (test_app.py)

### [v2.1] - Changed
- Dockerfile에 templates/ 디렉토리 복사 추가
- requirements.txt에 flask 추가

## [v2.0] - 2026-04-02

### [v2.0] - Added
- Docker Compose 멀티 서비스 구성 (generate, analyze, plot-capacity, plot-path-loss, test)
- 실행용 Dockerfile (루트)
- argparse CLI 인터페이스 (generate.py, analyze.py, plot_capacity.py, plot_path_loss.py)
- Makefile (pipeline, test, clean 등)
- CLI 테스트 (test_cli.py)
- data/ 디렉토리 (공유 볼륨)

### [v2.0] - Changed
- docker-compose.yml 재구성 (단일 서비스 → 멀티 서비스)
- analyze.py 리팩토링 (함수 분리)

## [v1.5] - 2026-04-01

### [v1.5] - Added
- CI/CD 파이프라인 구축 (GitHub Actions)
  - Black 포맷 검사 (lint job)
  - pytest 자동 실행 (test job, lint 통과 후 실행)
- 유닛 테스트 추가
  - `test_generate.py`: 시뮬레이션 데이터 생성 함수 테스트 (채널 행렬 shape/dtype, 경로 손실, 거리 범위 검증)
  - `test_numpy_channel.py`: Rayleigh 채널 및 채널 용량 계산 함수 테스트
- pytest 설정 (`pyproject.toml`)
- CI 배지를 README에 추가

### [v1.5] - Changed
- `generate.py` 코드 리팩토링 (함수 분리 및 구조 개선)
- `requirements.txt`에 테스트 의존성 추가 (`pytest`, `numpy`, `h5py`)

## [v1.0]

- 초기 릴리즈
- Rayleigh fading 채널 시뮬레이션
- 3GPP 경로 손실 모델
- HDF5 데이터 저장
- 시각화 기능
