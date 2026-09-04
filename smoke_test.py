from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]
PAGES = ["오늘", "업무 보드", "콘텐츠 캘린더", "언론·취재", "위기·이슈", "성과", "업무 기준"]


def main() -> None:
    app = AppTest.from_file(str(ROOT / "streamlit_app.py"), default_timeout=30)
    app.run()
    for page in PAGES:
        app.radio[0].set_value(page).run()
        if app.exception:
            messages = [error.message for error in app.exception]
            raise RuntimeError(f"{page} 화면 오류: {messages}")
        print(f"PASS: {page}")


if __name__ == "__main__":
    main()
