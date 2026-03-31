"""
논문용 Matplotlib 공통 스타일 설정 모듈

프로젝트 전반에서 일관된 그래프 스타일을 유지하기 위한 설정값과
유틸리티 함수를 제공합니다. 시뮬레이션 결과를 논문·보고서에 삽입할
품질(PDF 벡터, PNG 300 dpi)로 저장하는 것을 목적으로 합니다.

Usage:
    from plot_config import apply_style, save_figure, COLORS

    apply_style()
    fig, ax = plt.subplots()
    ax.plot(x, y, color=COLORS["primary"])
    save_figure(fig, "results/capacity_curve")
"""

import matplotlib.pyplot as plt

# Matplotlib rcParams 오버라이드 딕셔너리.
# apply_style() 호출 시 plt.rcParams 에 일괄 적용됩니다.
STYLE = {
    "font.size": 12,  # 기본 글꼴 크기 (pt)
    "font.family": "serif",  # 논문 표준 serif 계열 글꼴
    "figure.figsize": (8, 5),  # 기본 캔버스 크기 (인치)
    "axes.grid": True,  # 격자선 표시
    "grid.alpha": 0.3,  # 격자선 투명도
    "lines.linewidth": 1.5,  # 선 두께 (pt)
    "lines.markersize": 6,  # 마커 크기 (pt)
    "legend.fontsize": 10,  # 범례 글꼴 크기 (pt)
    "axes.labelsize": 13,  # 축 레이블 글꼴 크기 (pt)
    "xtick.labelsize": 11,  # x축 눈금 글꼴 크기 (pt)
    "ytick.labelsize": 11,  # y축 눈금 글꼴 크기 (pt)
}

# Matplotlib 기본 색상 사이클과 대응하는 프로젝트 공용 색상 팔레트.
# 곡선·계열이 늘어날 경우 이 딕셔너리에 키를 추가하세요.
COLORS = {
    "primary": "#1f77b4",  # 파랑  — 첫 번째 계열
    "secondary": "#ff7f0e",  # 주황  — 두 번째 계열
    "tertiary": "#2ca02c",  # 초록  — 세 번째 계열
    "quaternary": "#d62728",  # 빨강  — 네 번째 계열
}


def apply_style():
    """프로젝트 공용 논문 스타일을 Matplotlib 전역 설정에 적용합니다.

    STYLE 딕셔너리의 값을 plt.rcParams 에 일괄 업데이트합니다.
    그래프를 그리기 전, 스크립트 최상단에서 한 번만 호출하면 됩니다.

    Returns
    -------
    None
    """
    plt.rcParams.update(STYLE)


def save_figure(fig, filename, formats=("pdf", "png")):
    """Figure를 논문 제출용 포맷으로 저장합니다.

    - PDF: 벡터 그래픽, dpi 설정 없음 (무손실 확대 가능)
    - PNG: 래스터 그래픽, 300 dpi (인쇄 품질)

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        저장할 Figure 객체
    filename : str
        확장자를 제외한 저장 경로 및 파일명
        (예: "results/capacity_curve" → "results/capacity_curve.pdf" 등)
    formats : tuple of str, optional
        저장할 포맷 목록. 기본값은 ("pdf", "png")

    Returns
    -------
    None
    """
    for fmt in formats:
        filepath = f"{filename}.{fmt}"
        dpi = 300 if fmt == "png" else None
        fig.savefig(filepath, bbox_inches="tight", dpi=dpi)
        print(f"  저장: {filepath}")


def create_subplots(n_cols, fig_width_per_col=5, height=4):
    """논문용 서브플롯을 가로로 배열하여 생성합니다.

    apply_style()을 내부적으로 호출하므로 별도 스타일 적용이 필요 없습니다.
    n_cols=1인 경우에도 axes를 리스트로 반환하여 일관된 인터페이스를 제공합니다.

    Parameters
    ----------
    n_cols : int
        가로 방향 서브플롯 수
    fig_width_per_col : float, optional
        서브플롯 하나당 Figure 너비 (인치). 기본값은 5.
        전체 Figure 너비 = fig_width_per_col * n_cols
    height : float, optional
        Figure 높이 (인치). 기본값은 4.

    Returns
    -------
    fig : matplotlib.figure.Figure
        생성된 Figure 객체
    axes : list of matplotlib.axes.Axes
        길이 n_cols인 Axes 리스트
    """
    apply_style()
    fig, axes = plt.subplots(1, n_cols, figsize=(fig_width_per_col * n_cols, height))
    if n_cols == 1:
        axes = [axes]
    return fig, axes
