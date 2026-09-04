from __future__ import annotations

import json
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "demo_work_items.json"

STATUSES = ["접수", "기획", "제작", "검토", "승인", "배포", "완료"]
TYPES = ["보도자료", "언론취재", "SNS", "영상", "행사", "사내홍보", "위기이슈"]

CHECKLISTS = {
    "보도자료": ["사실·수치 원출처 확인", "제목에 핵심 뉴스 반영", "관계부서 팩트체크", "초상권·개인정보 확인", "배포처·기자 리스트 확정", "최종 승인본 잠금"],
    "언론취재": ["취재 목적·질문지 확보", "인터뷰이·장소 확정", "예상 질의응답 작성", "촬영 동선·보안구역 확인", "현장 담당자 공유", "보도 결과 모니터링"],
    "SNS": ["타깃과 행동목표 정의", "첫 문장 후킹 확인", "이미지·영상 규격 확인", "맞춤법·링크 검수", "게시 시간 확정", "댓글·반응 모니터링"],
    "영상": ["기획의도·한 문장 메시지", "콘티·대본 승인", "출연·촬영 동의", "안전·브랜드 가이드 확인", "자막·음원 저작권 확인", "썸네일·배포 채널 확정"],
    "행사": ["목적·참석 대상 확정", "장소·동선·안전 확인", "내빈·의전 명단 확인", "사진·영상 촬영계획", "보도자료·SNS 연계", "종료 후 결과보고"],
    "사내홍보": ["공지 대상 세분화", "현업 용어를 쉬운 표현으로 수정", "게시 채널·시간 확정", "민감정보·보안 확인", "문의 담당자 표기", "조회·반응 확인"],
    "위기이슈": ["확인된 사실/추정 분리", "1차 보고 완료", "대응 책임자 지정", "홀딩 스테이트먼트 작성", "대외 창구 일원화", "종결 후 재발방지 기록"],
}

PLAYBOOKS = [
    ("📰", "보도자료", "기획안 · 팩트체크 · 인용문 · 배포명단 · 성과보고"),
    ("🎤", "취재 대응", "질문지 · 예상 Q&A · 동선 · 인터뷰이 브리핑 · 결과보고"),
    ("🚨", "위기 커뮤니케이션", "사실확인 · 보고선 · 홀딩문 · 채널 일원화 · 사후 회고"),
    ("🎬", "영상·SNS", "기획 · 콘티 · 검수 · 저작권 · 게시 · 댓글 대응"),
    ("🎪", "행사·의전", "초청 · 의전 · 안전 · 촬영 · 현장운영 · 결과 정리"),
    ("📊", "월간 성과보고", "도달 · 반응 · 핵심 메시지 · 긍부정 · 개선안"),
]

LESSONS = [
    ("팩트체크", "수치가 바뀌는 순간부터 버전이 갈라집니다.", "최종 수치의 원출처·확인자·확인시간을 같은 업무 카드에 남깁니다.", "배포 30분 전 숫자·고유명사 재확인"),
    ("승인", "메신저 승인만 믿으면 최종본이 섞입니다.", "승인된 파일과 수정 중 파일을 분리하고 최종 승인자·시간을 기록합니다.", "승인본 수정 시 재승인"),
    ("현장", "행사 당일은 작은 누락이 크게 보입니다.", "내빈 성명·직함·좌석·촬영 포인트를 전날 한 장으로 공유합니다.", "D-1 현장 점검, H-2 브리핑"),
    ("콘텐츠", "좋은 내용도 첫 문장이 약하면 읽히지 않습니다.", "대상과 기대 행동을 먼저 정하고 제목·썸네일을 별도 검수합니다.", "한 콘텐츠에 핵심 메시지 하나"),
]


def _default_items() -> list[dict[str, Any]]:
    return [
        {
            "id": "PR-260903-01", "title": "지역상생 의료봉사 보도자료", "type": "보도자료",
            "status": "검토", "priority": "높음", "owner": "조진우", "due_date": "2026-09-04",
            "channel": "언론·홈페이지", "requester": "사회공헌팀", "objective": "지역상생 활동의 신뢰도 제고",
            "audience": "지역 언론·시민", "key_message": "의료 접근성이 낮은 지역에 지속 가능한 진료 지원",
            "risk": "수혜자 개인정보 및 사진 동의", "memo": "진료 인원 수치 재확인 필요", "progress": 67,
            "checklist": make_checklist("보도자료", 3),
        },
        {
            "id": "PR-260903-02", "title": "건강정보 숏폼: 거품뇨 편", "type": "영상",
            "status": "제작", "priority": "보통", "owner": "김민지", "due_date": "2026-09-06",
            "channel": "유튜브·인스타그램", "requester": "신장내과", "objective": "정확한 건강정보 확산",
            "audience": "30~50대 일반인", "key_message": "거품뇨가 반복되면 단백뇨 검사가 필요할 수 있다",
            "risk": "의학적 단정 표현 금지", "memo": "의료진 감수 후 자막 확정", "progress": 48,
            "checklist": make_checklist("영상", 2),
        },
        {
            "id": "PR-260903-03", "title": "신규 센터 개소식 취재 지원", "type": "행사",
            "status": "기획", "priority": "높음", "owner": "박서준", "due_date": "2026-09-08",
            "channel": "행사·언론·사내", "requester": "기획조정실", "objective": "센터 전문성과 개소 의미 전달",
            "audience": "언론·내빈·구성원", "key_message": "진료와 연구를 잇는 지역 거점",
            "risk": "내빈 순서와 명칭 오류", "memo": "의전안 확정 대기", "progress": 31,
            "checklist": make_checklist("행사", 1),
        },
        {
            "id": "PR-260903-04", "title": "온라인 커뮤니티 오정보 대응", "type": "위기이슈",
            "status": "승인", "priority": "긴급", "owner": "조진우", "due_date": "2026-09-03",
            "channel": "온라인·언론", "requester": "홍보실", "objective": "확산 차단 및 사실관계 정정",
            "audience": "환자·보호자·언론", "key_message": "확인된 사실과 공식 조치 중심으로 안내",
            "risk": "개별 환자정보 노출·감정적 대응", "memo": "법무 검토 완료, 원장 승인 대기", "progress": 84,
            "checklist": make_checklist("위기이슈", 4),
        },
        {
            "id": "PR-260903-05", "title": "추석 연휴 진료 안내 카드뉴스", "type": "SNS",
            "status": "배포", "priority": "보통", "owner": "김민지", "due_date": "2026-09-05",
            "channel": "인스타그램·블로그", "requester": "원무팀", "objective": "연휴 이용 혼선 최소화",
            "audience": "환자·보호자", "key_message": "진료 일정과 응급 이용 방법을 한눈에",
            "risk": "운영시간 변경 가능성", "memo": "당일 오전 최종 시간 확인", "progress": 93,
            "checklist": make_checklist("SNS", 6),
        },
    ]


def make_checklist(work_type: str, done_count: int = 0) -> list[dict[str, Any]]:
    return [
        {"label": label, "done": index < done_count}
        for index, label in enumerate(CHECKLISTS[work_type])
    ]


def load_initial_data() -> list[dict[str, Any]]:
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return _default_items()


def ensure_state() -> None:
    if "work_items" not in st.session_state:
        st.session_state.work_items = deepcopy(load_initial_data())
    if "flash" not in st.session_state:
        st.session_state.flash = ""


def add_item(payload: dict[str, Any]) -> None:
    item = {
        "id": f"PR-{date.today().strftime('%y%m%d')}-{len(st.session_state.work_items) + 1:02d}",
        "title": payload["title"].strip(),
        "type": payload["type"],
        "status": "접수",
        "priority": payload["priority"],
        "owner": payload["owner"].strip(),
        "due_date": payload["due_date"].isoformat(),
        "channel": payload["channel"].strip(),
        "requester": payload["requester"].strip(),
        "objective": payload["objective"].strip(),
        "audience": payload["audience"].strip(),
        "key_message": payload["key_message"].strip(),
        "risk": payload["risk"].strip(),
        "memo": "",
        "progress": 5,
        "checklist": make_checklist(payload["type"]),
    }
    st.session_state.work_items.insert(0, item)
    st.session_state.flash = "새 업무가 접수되었습니다. 🌱"


def update_item(item_id: str, **changes: Any) -> None:
    for index, item in enumerate(st.session_state.work_items):
        if item["id"] == item_id:
            updated = {**item, **changes}
            st.session_state.work_items[index] = updated
            return


def delete_item(item_id: str) -> None:
    st.session_state.work_items = [item for item in st.session_state.work_items if item["id"] != item_id]
    st.session_state.flash = "업무가 삭제되었습니다."


def move_next(item_id: str) -> None:
    item = next((row for row in st.session_state.work_items if row["id"] == item_id), None)
    if not item:
        return
    index = STATUSES.index(item["status"])
    if index < len(STATUSES) - 1:
        next_status = STATUSES[index + 1]
        update_item(item_id, status=next_status, progress=100 if next_status == "완료" else min(95, item["progress"] + 15))
        st.session_state.flash = f"{next_status} 단계로 이동했습니다. 🐚"


def export_json() -> str:
    return json.dumps(st.session_state.work_items, ensure_ascii=False, indent=2)


def import_json(raw: bytes) -> tuple[bool, str]:
    try:
        payload = json.loads(raw.decode("utf-8"))
        items = payload.get("items", payload) if isinstance(payload, dict) else payload
        if not isinstance(items, list):
            raise ValueError
        st.session_state.work_items = items
        return True, f"업무 {len(items)}건을 불러왔습니다."
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError, AttributeError):
        return False, "올바른 PR Flow JSON 파일이 아닙니다."
