from __future__ import annotations

import base64
from html import escape
from io import BytesIO
from pathlib import Path

import streamlit as st

from embedded_assets import LITTLE_SISTER_B64, SEA_POEM_B64

BASE_DIR = Path(__file__).parent


def _asset_b64(path: Path, fallback_b64: str) -> str:
    """Return the original asset when available, otherwise its built-in copy."""
    try:
        return base64.b64encode(path.read_bytes()).decode("ascii")
    except (FileNotFoundError, OSError):
        return fallback_b64


def _data_uri(path: Path, fallback_b64: str) -> str:
    return f"data:image/jpeg;base64,{_asset_b64(path, fallback_b64)}"


def _image_source(path: Path, fallback_b64: str) -> Path | BytesIO:
    """Build a Streamlit image source that is safe on GitHub deployments."""
    if path.is_file():
        return path
    return BytesIO(base64.b64decode(fallback_b64))


def inject_css() -> None:
    sea = _data_uri(BASE_DIR / "assets" / "sea_poem.jpeg", SEA_POEM_B64)
    sister = _data_uri(BASE_DIR / "assets" / "little_sister.jpeg", LITTLE_SISTER_B64)
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
        :root {{
            --sea: #207f82;
            --deep-sea: #15585e;
            --sky: #d9f0ef;
            --sun: #e7ad31;
            --pink: #ef6f88;
            --cream: #fffaf0;
            --ink: #263837;
            --muted: #6e7e7c;
        }}
        html, body, [class*="css"] {{ font-family: 'Noto Sans KR', sans-serif; }}
        .stApp {{ background: linear-gradient(180deg, #f9fffe 0%, #fffaf2 100%); color: var(--ink); }}
        [data-testid="stHeader"] {{ background: transparent; }}
        [data-testid="stSidebar"] {{ background: linear-gradient(180deg, #176d70 0%, #104f56 100%); border-right: 0; }}
        [data-testid="stSidebar"] * {{ color: white; }}
        [data-testid="stSidebar"] [data-testid="stImage"] img {{ border-radius: 22px; border: 4px solid #ffffff4d; box-shadow: 0 12px 30px #0a343b70; }}
        [data-testid="stSidebar"] .stRadio label {{ padding: .48rem .65rem; border-radius: 12px; transition: .18s; }}
        [data-testid="stSidebar"] .stRadio label:hover {{ background: #ffffff18; }}
        [data-testid="stSidebar"] .stButton button {{ border: 1px solid #ffffff40; background: #ffffff14; color: white; }}
        [data-testid="stSidebar"] .stDownloadButton button {{ border: 1px solid #ffffff40; background: #ffffff14; color: white; }}
        [data-testid="stSidebar"] small {{ color: #c4e2e0 !important; }}
        .block-container {{ max-width: 1480px; padding-top: 2rem; padding-bottom: 4rem; }}
        h1, h2, h3 {{ letter-spacing: -0.04em; color: var(--ink); }}
        .cute-title {{ font-family: 'Gaegu', cursive; font-weight: 700; font-size: 2.2rem; line-height: 1; color: #fff6cc; margin: .3rem 0 .1rem; }}
        .cute-sub {{ color: #d5eeec; font-size: .75rem; line-height: 1.45; margin-bottom: 1rem; }}
        .hero {{
            position: relative; overflow: hidden; min-height: 190px; border-radius: 28px;
            background-image: linear-gradient(90deg, #0d555be8 0%, #14777ed0 45%, #1d7b7f55 100%), url('{sea}');
            background-size: cover; background-position: center 44%; padding: 32px 34px; color: white;
            box-shadow: 0 16px 42px #18595c25; margin-bottom: 1.4rem;
        }}
        .hero::after {{ content: ''; position: absolute; width: 170px; height: 170px; border-radius: 50%; background: #f2bd4640; right: -35px; top: -50px; }}
        .hero-kicker {{ color: #ffdc78; text-transform: uppercase; letter-spacing: .14em; font-size: .72rem; font-weight: 800; }}
        .hero h1 {{ font-family: 'Gaegu', cursive; color: white; font-size: 3rem; margin: .25rem 0 .35rem; letter-spacing: -.03em; }}
        .hero p {{ max-width: 680px; margin: 0; color: #e3f5f3; line-height: 1.65; font-size: .92rem; }}
        .hero-chip {{ display: inline-flex; margin-top: 1rem; padding: .38rem .75rem; border-radius: 999px; background: #fff5d5; color: #6a5421; font-size: .73rem; font-weight: 700; }}
        .section-kicker {{ color: var(--sea); font-weight: 800; font-size: .72rem; text-transform: uppercase; letter-spacing: .12em; margin: .25rem 0; }}
        .section-title {{ font-size: 1.48rem; font-weight: 800; margin-bottom: .2rem; }}
        .section-desc {{ color: var(--muted); font-size: .83rem; margin-bottom: 1.1rem; }}
        .metric-card {{ background: #fff; border: 1px solid #dce9e7; border-radius: 20px; padding: 1.15rem 1.1rem; box-shadow: 0 8px 24px #235f5c0d; min-height: 120px; position: relative; overflow: hidden; }}
        .metric-card::after {{ content: ''; position: absolute; width: 68px; height: 68px; border-radius: 50%; right: -22px; bottom: -24px; background: var(--accent, #d9f0ef); opacity: .65; }}
        .metric-card .icon {{ font-size: 1.35rem; }}
        .metric-card .label {{ color: var(--muted); font-size: .75rem; margin-top: .55rem; }}
        .metric-card .value {{ color: var(--ink); font-size: 1.75rem; font-weight: 800; line-height: 1.1; }}
        .metric-card .note {{ color: #8a9997; font-size: .66rem; }}
        .task-card {{ background: #fff; border: 1px solid #dce9e7; border-radius: 18px; padding: 1rem 1.05rem; box-shadow: 0 7px 20px #235f5c0d; margin-bottom: .7rem; }}
        .task-card.urgent {{ border: 2px solid #f0a1ad; background: #fff9fa; }}
        .badges {{ display: flex; flex-wrap: wrap; gap: .35rem; margin-bottom: .55rem; }}
        .badge {{ border-radius: 999px; padding: .2rem .55rem; font-size: .67rem; font-weight: 700; background: #e4f3f1; color: #176d70; }}
        .badge.pink {{ background: #ffedf1; color: #b53f5b; }}
        .badge.sun {{ background: #fff4d8; color: #8c6513; }}
        .task-title {{ font-size: .98rem; font-weight: 800; margin-bottom: .25rem; color: var(--ink); }}
        .task-message {{ font-size: .78rem; color: var(--muted); line-height: 1.55; min-height: 2.4rem; }}
        .task-meta {{ display: flex; flex-wrap: wrap; gap: .65rem; font-size: .68rem; color: #81908f; margin-top: .6rem; }}
        .mini-progress {{ height: 7px; border-radius: 99px; background: #e8efee; overflow: hidden; margin-top: .65rem; }}
        .mini-progress span {{ display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, #27888a, #e2ae3d); }}
        .stButton button, .stDownloadButton button {{ border-radius: 12px; font-weight: 700; min-height: 2.55rem; }}
        .stButton button[kind="primary"] {{ background: var(--sea); border-color: var(--sea); }}
        div[data-baseweb="select"] > div, .stTextInput input, .stDateInput input, .stTextArea textarea {{ border-radius: 12px !important; }}
        [data-testid="stExpander"] {{ background: white; border: 1px solid #dce9e7; border-radius: 16px; box-shadow: 0 6px 20px #235f5c0a; overflow: hidden; }}
        [data-testid="stMetric"] {{ background: white; border: 1px solid #dce9e7; border-radius: 18px; padding: 1rem; }}
        [data-testid="stMetricValue"] {{ color: var(--deep-sea); }}
        [data-testid="stTabs"] button {{ font-weight: 700; }}
        .soft-panel {{ background: #fff; border: 1px solid #dce9e7; border-radius: 20px; padding: 1.15rem 1.25rem; margin: .7rem 0; }}
        .warning-panel {{ background: #fff1f3; border: 1px solid #f5c4cd; border-radius: 18px; padding: 1rem 1.2rem; color: #8a3446; margin-bottom: 1rem; }}
        .playbook {{ min-height: 165px; background: white; border: 1px solid #dce9e7; border-radius: 20px; padding: 1rem; box-shadow: 0 8px 22px #235f5c0b; }}
        .playbook .emoji {{ font-size: 1.5rem; }}
        .playbook h3 {{ font-size: .98rem; margin: .4rem 0; }}
        .playbook p {{ color: var(--muted); font-size: .75rem; line-height: 1.55; }}
        .sister-note {{ background-image: linear-gradient(90deg, #0f6263ee, #0f6263aa), url('{sister}'); background-size: cover; background-position: center 75%; border-radius: 20px; padding: 1.2rem; color: white; min-height: 130px; margin-top: 1rem; }}
        .sister-note b {{ font-family: 'Gaegu', cursive; font-size: 1.55rem; color: #ffdb65; }}
        .sister-note p {{ max-width: 65%; font-size: .75rem; color: #e5f5f3; }}
        .empty-state {{ text-align: center; background: #fff; border: 2px dashed #cde2df; border-radius: 22px; padding: 2.5rem 1rem; color: var(--muted); }}
        .foot-note {{ text-align: center; color: #82918f; font-size: .68rem; padding-top: 2.3rem; }}
        @media (max-width: 760px) {{
            .block-container {{ padding: 1.2rem .9rem 3rem; }}
            .hero {{ min-height: 175px; border-radius: 22px; padding: 24px 20px; background-position: center; }}
            .hero h1 {{ font-size: 2.35rem; }}
            .hero p {{ font-size: .8rem; max-width: 92%; }}
            .metric-card {{ min-height: 105px; margin-bottom: .35rem; }}
            .task-title {{ font-size: .92rem; }}
            .sister-note p {{ max-width: 90%; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    st.markdown('<div class="cute-title">🌊 홍보 바다</div>', unsafe_allow_html=True)
    st.markdown('<div class="cute-sub">업무가 파도처럼 밀려와도<br>하나씩 예쁘게 정리해요.</div>', unsafe_allow_html=True)
    st.image(
        _image_source(BASE_DIR / "assets" / "little_sister.jpeg", LITTLE_SISTER_B64),
        width="stretch",
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
            <div class="hero-kicker">COMMUNICATIONS WORKSPACE</div>
            <h1>오늘도, 홍보는 맑음 ☀️</h1>
            <p>요청부터 기획·제작·승인·배포·회고까지 한 흐름으로 관리하고,<br>작은 실수는 다음 업무의 좋은 기준으로 바꿉니다.</p>
            <span class="hero-chip">바다처럼 넓게 보고 · 조개처럼 꼼꼼하게</span>
        </section>
        """,
        unsafe_allow_html=True,
    )


def section_heading(kicker: str, title: str, description: str = "") -> None:
    st.markdown(
        f'<div class="section-kicker">{kicker}</div><div class="section-title">{title}</div><div class="section-desc">{description}</div>',
        unsafe_allow_html=True,
    )


def metric_card(icon: str, label: str, value: str, note: str, accent: str) -> str:
    return f"""
    <div class="metric-card" style="--accent:{accent}">
        <div class="icon">{icon}</div><div class="label">{label}</div>
        <div class="value">{value}</div><div class="note">{note}</div>
    </div>
    """


def task_card(item: dict) -> str:
    urgent = " urgent" if item["priority"] == "긴급" else ""
    priority_class = "pink" if item["priority"] == "긴급" else "sun"
    work_type = escape(str(item["type"]))
    priority = escape(str(item["priority"]))
    status = escape(str(item["status"]))
    title = escape(str(item["title"]))
    message = escape(str(item["key_message"] or "핵심 메시지를 입력해 주세요."))
    owner = escape(str(item["owner"]))
    due_date = escape(str(item["due_date"]))
    channel = escape(str(item["channel"]))
    return f"""
    <div class="task-card{urgent}">
        <div class="badges"><span class="badge">{work_type}</span><span class="badge {priority_class}">{priority}</span><span class="badge">{status}</span></div>
        <div class="task-title">{title}</div>
        <div class="task-message">{message}</div>
        <div class="task-meta"><span>👤 {owner}</span><span>📅 {due_date}</span><span>📣 {channel}</span></div>
        <div class="mini-progress"><span style="width:{item['progress']}%"></span></div>
    </div>
    """
