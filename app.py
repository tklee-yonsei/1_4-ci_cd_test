"""
시뮬레이션 웹 API 서버
"""

import os
from flask import Flask, jsonify, request, send_from_directory
from generate import generate_scenario, save_to_hdf5
from analyze import load_and_analyze, plot_analysis

app = Flask(__name__)

# 결과 파일 저장 경로
DATA_DIR = os.environ.get("DATA_DIR", "/app/data")
os.makedirs(DATA_DIR, exist_ok=True)


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/api/generate", methods=["POST"])
def api_generate():
    """시뮬레이션 데이터 생성

    Request JSON:
        {
            "n_scenarios": 50,
            "n_samples": 200,
            "frequencies": [3.5, 28, 60],
            "output": "simulation.h5"
        }
    """
    data = request.get_json() or {}
    n_scenarios = data.get("n_scenarios", 50)
    n_samples = data.get("n_samples", 200)
    frequencies_ghz = data.get("frequencies", [3.5, 28, 60])
    output = data.get("output", "simulation.h5")

    frequencies = [f * 1e9 for f in frequencies_ghz]
    output_path = os.path.join(DATA_DIR, output)

    # 데이터 생성
    scenarios_data = {}
    for freq in frequencies:
        scenarios_data[freq] = [
            generate_scenario(n_samples, freq=freq) for _ in range(n_scenarios)
        ]

    save_to_hdf5(output_path, scenarios_data, frequencies)

    file_size_mb = os.path.getsize(output_path) / 1024 / 1024

    return jsonify(
        {
            "status": "success",
            "n_scenarios": n_scenarios * len(frequencies),
            "output": output,
            "file_size_mb": round(file_size_mb, 2),
        }
    )


@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """데이터 분석 및 그래프 생성

    Request JSON:
        {
            "input": "simulation.h5",
            "output": "analysis_result",
            "snr": 20
        }
    """
    data = request.get_json() or {}
    input_file = data.get("input", "simulation.h5")
    output_prefix = data.get("output", "analysis_result")
    snr_db = data.get("snr", 20)

    input_path = os.path.join(DATA_DIR, input_file)
    output_path = os.path.join(DATA_DIR, output_prefix)

    if not os.path.exists(input_path):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Input file not found: {input_file}",
                }
            ),
            404,
        )

    freq_data = load_and_analyze(input_path, snr_db=snr_db)
    plot_analysis(freq_data, output_path)

    # 주파수별 요약 통계
    summary = {}
    for name, d in freq_data.items():
        summary[name] = {
            "n_samples": len(d["path_loss"]),
            "avg_path_loss_db": round(float(d["path_loss"].mean()), 2),
            "avg_capacity_bps_hz": round(float(d["capacity"].mean()), 2),
        }

    return jsonify(
        {
            "status": "success",
            "output_png": f"{output_prefix}.png",
            "output_pdf": f"{output_prefix}.pdf",
            "summary": summary,
        }
    )


@app.route("/api/results")
def api_results():
    """결과 파일 목록 조회"""
    if not os.path.exists(DATA_DIR):
        return jsonify({"files": []})

    files = []
    for filename in sorted(os.listdir(DATA_DIR)):
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.isfile(filepath) and not filename.startswith("."):
            files.append(
                {
                    "name": filename,
                    "size_kb": round(os.path.getsize(filepath) / 1024, 1),
                }
            )
    return jsonify({"files": files})


@app.route("/api/results/<path:filename>")
def api_result_file(filename):
    """결과 파일 다운로드 (이미지 등)"""
    return send_from_directory(DATA_DIR, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
