"""
시뮬레이션 웹 API 서버

Flask 기반으로 브라우저에서 시뮬레이션을 실행하고
결과를 확인할 수 있는 웹 인터페이스를 제공합니다.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return "Telecom Simulation API"


@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
