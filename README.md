# 홍보 바다 — PR Flow Streamlit

홍보 업무를 `접수 → 기획 → 제작 → 검토 → 승인 → 배포 → 완료` 흐름으로 관리하는 Streamlit 앱입니다. 사용자가 제공한 바다 그림과 동생 그림의 청록·노랑·분홍 색감을 UI에 반영했습니다.

## GitHub에 올릴 파일

저장소 최상단에 아래 구조가 그대로 보이도록 업로드하세요.

```text
PR-Flow-Streamlit/
├── streamlit_app.py
├── app_data.py
├── app_styles.py
├── requirements.txt
├── README.md
├── .gitignore
├── .github/workflows/
│   └── streamlit-smoke-test.yml
├── .streamlit/
│   └── config.toml
├── assets/
│   ├── sea_poem.jpeg
│   └── little_sister.jpeg
└── data/
    └── demo_work_items.json
```

## Streamlit Community Cloud 연결

1. GitHub에서 새 저장소를 만들고 이 폴더의 **내용 전체**를 업로드합니다.
2. <https://share.streamlit.io>에 GitHub 계정으로 로그인합니다.
3. **Create app → Yup, I have an app**을 선택합니다.
4. Repository는 방금 만든 저장소, Branch는 `main`을 선택합니다.
5. Main file path에 `streamlit_app.py`를 입력합니다.
6. **Deploy**를 누릅니다.

GitHub의 `main` 브랜치 코드를 수정하면 Streamlit 앱에도 자동 반영됩니다.
또한 GitHub Actions가 모든 화면의 기동 여부를 자동 검사합니다.

## 내 컴퓨터에서 실행

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## 데이터 저장 방식

- 업무는 현재 접속 세션에서 편집됩니다.
- 사이드바의 **JSON 백업**으로 업무를 내려받을 수 있습니다.
- 다음 접속 때 **백업 불러오기**로 복원할 수 있습니다.
- 여러 직원이 같은 데이터를 동시에 사용하려면 Supabase·Google Sheets·사내 DB 중 하나를 다음 단계에서 연결하세요.

## 주요 기능

- 오늘의 우선업무와 긴급·승인 대기 표시
- 업무 유형별 자동 체크리스트
- 단계·우선순위·진척도·메모 수정
- 콘텐츠 일정과 채널별 업무 분포
- 언론·취재 전용 관리 화면
- 위기이슈 대응 7단계
- 성과지표와 재발방지 기준
- JSON 백업·불러오기
- 모바일·PC 반응형 테마
