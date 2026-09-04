from __future__ import annotations

from datetime import date, datetime, timedelta
from html import escape

import pandas as pd
import streamlit as st

from app_data import (
    CHECKLISTS,
    LESSONS,
    PLAYBOOKS,
    STATUSES,
    TYPES,
    add_item,
    delete_item,
    ensure_state,
    export_json,
    import_json,
    move_next,
    update_item,
)
from app_styles import inject_css, metric_card, render_hero, render_sidebar_brand, section_heading, task_card

st.set_page_config(
    page_title="홍보 바다 | PR Flow",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()
ensure_state()


@st.dialog("새 홍보 업무 접수 🌱", width="large")
def create_work_dialog() -> None:
    st.caption("요청받은 일을 바로 시작하지 말고 목적·대상·핵심 메시지·마감을 먼저 정리해요.")
    with st.form("create_work_form"):
        left, right = st.columns(2)
        with left:
            work_type = st.selectbox("업무 유형", TYPES)
            owner = st.text_input("담당자", value="조진우")
            requester = st.text_input("요청부서", value="홍보실")
            audience = st.text_input("핵심 대상", placeholder="예: 지역 언론·시민")
        with right:
            priority = st.selectbox("우선순위", ["보통", "높음", "긴급"])
            due_date = st.date_input("마감일", value=date.today() + timedelta(days=3))
            channel = st.text_input("배포 채널", value="언론·홈페이지")
            risk = st.text_input("주의할 위험", placeholder="개인정보, 수치, 저작권 등")
        title = st.text_input("업무명 *", placeholder="예: 신규 센터 개소 보도자료")
        objective = st.text_input("업무 목적", placeholder="이 업무로 무엇을 바꾸려는가")
        key_message = st.text_area("핵심 메시지", placeholder="대상이 반드시 기억해야 할 한 문장")
        st.info(f"{work_type} 기본 체크리스트 {len(CHECKLISTS[work_type])}개가 자동으로 붙습니다.", icon="🐚")
        submitted = st.form_submit_button("업무 등록하기", type="primary", width="stretch")
        if submitted:
            if not title.strip():
                st.error("업무명을 입력해 주세요.")
                return
            add_item(
                {
                    "title": title, "type": work_type, "priority": priority, "owner": owner,
                    "due_date": due_date, "channel": channel, "requester": requester,
                    "objective": objective, "audience": audience, "key_message": key_message, "risk": risk,
                }
            )
            st.rerun()


def show_flash() -> None:
    if st.session_state.flash:
        st.toast(st.session_state.flash, icon="🌊")
        st.session_state.flash = ""


def task_controls(item: dict, prefix: str) -> None:
    with st.expander("업무 상세·체크리스트 열기"):
        top1, top2, top3 = st.columns([1.1, 1.1, 1])
        new_status = top1.selectbox("현재 단계", STATUSES, index=STATUSES.index(item["status"]), key=f"{prefix}_status_{item['id']}")
        progress = top2.slider("진척도", 0, 100, int(item["progress"]), key=f"{prefix}_progress_{item['id']}")
        priority = top3.selectbox("우선순위", ["보통", "높음", "긴급"], index=["보통", "높음", "긴급"].index(item["priority"]), key=f"{prefix}_priority_{item['id']}")
        if new_status != item["status"] or progress != item["progress"] or priority != item["priority"]:
            update_item(item["id"], status=new_status, progress=100 if new_status == "완료" else progress, priority=priority)

        st.markdown("##### 필수 체크리스트")
        updated_checks = []
        for index, check in enumerate(item["checklist"]):
            checked = st.checkbox(check["label"], value=check["done"], key=f"{prefix}_check_{item['id']}_{index}")
            updated_checks.append({"label": check["label"], "done": checked})
        if updated_checks != item["checklist"]:
            update_item(item["id"], checklist=updated_checks)

        memo = st.text_area("결정사항·수정 사유·다음 행동", value=item.get("memo", ""), key=f"{prefix}_memo_{item['id']}")
        if memo != item.get("memo", ""):
            update_item(item["id"], memo=memo)

        c1, c2 = st.columns([2, 1])
        if c1.button("다음 단계로", key=f"{prefix}_next_{item['id']}", type="primary", width="stretch"):
            move_next(item["id"])
            st.rerun()
        if c2.button("삭제", key=f"{prefix}_delete_{item['id']}", width="stretch"):
            delete_item(item["id"])
            st.rerun()


def dashboard_page(items: list[dict]) -> None:
    render_hero()
    active = len([row for row in items if row["status"] != "완료"])
    urgent = len([row for row in items if row["priority"] == "긴급" and row["status"] != "완료"])
    approval = len([row for row in items if row["status"] in {"검토", "승인"}])
    average = round(sum(row["progress"] for row in items) / max(len(items), 1))
    cols = st.columns(4)
    cards = [
        ("🫧", "진행 업무", str(active), "전체 파이프라인", "#d7f0ee"),
        ("🚨", "긴급 대응", str(urgent), "즉시 확인 필요", "#ffdce3"),
        ("⏳", "검토·승인", str(approval), "막힌 업무 확인", "#fff0bd"),
        ("🐚", "평균 진척도", f"{average}%", "이번 주 기준", "#dce8fb"),
    ]
    for column, card in zip(cols, cards):
        column.markdown(metric_card(*card), unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.55, 1])
    attention = [row for row in items if row["priority"] == "긴급" or row["status"] in {"검토", "승인"}]
    with left:
        section_heading("ACTION CENTER", "지금 처리할 업무", "긴급·검토·승인 업무를 먼저 보여줍니다.")
        if not attention:
            st.markdown('<div class="empty-state">🌤️ 지금 급하게 처리할 업무가 없어요.</div>', unsafe_allow_html=True)
        for item in attention:
            st.markdown(task_card(item), unsafe_allow_html=True)
            task_controls(item, "today")
    with right:
        section_heading("DAILY DISCIPLINE", "퇴근 전 5분 점검", "오늘의 기록을 내일의 여유로 바꿔요.")
        checks = [
            "내일 마감 업무의 자료·승인자 확인", "배포 콘텐츠 링크와 최종본 저장",
            "언론·온라인 언급 이상징후 확인", "결정사항과 수정 사유 기록", "미완료 업무의 다음 행동 지정",
        ]
        done = 0
        with st.container(border=True):
            for index, text in enumerate(checks):
                if st.checkbox(text, value=index < 2, key=f"daily_{index}"):
                    done += 1
            st.progress(done / len(checks), text=f"오늘 기록 완성도 {done}/{len(checks)}")
        st.markdown(
            '<div class="sister-note"><b>하나뿐인 귀여운 홍보팀 🌼</b><p>급한 일도 잘하고, 기록도 잘하면 다음 업무가 조금 더 가벼워져요.</p></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    section_heading("WORKFLOW PULSE", "업무 흐름", "어느 단계에 일이 몰렸는지 한눈에 확인합니다.")
    flow_columns = st.columns(7)
    for column, status in zip(flow_columns, STATUSES):
        count = len([row for row in items if row["status"] == status])
        column.metric(status, count)


def board_page(items: list[dict]) -> None:
    section_heading("INTEGRATED PIPELINE", "🌊 업무 보드", "접수부터 완료까지 업무가 막힌 위치를 확인합니다.")
    tabs = st.tabs([f"{status} · {len([i for i in items if i['status'] == status])}" for status in STATUSES])
    for tab, status in zip(tabs, STATUSES):
        with tab:
            rows = [row for row in items if row["status"] == status]
            if not rows:
                st.markdown('<div class="empty-state">이 단계에서 기다리는 업무가 없어요. 🐠</div>', unsafe_allow_html=True)
            columns = st.columns(2)
            for index, item in enumerate(rows):
                with columns[index % 2]:
                    st.markdown(task_card(item), unsafe_allow_html=True)
                    task_controls(item, f"board_{status}")


def calendar_page(items: list[dict]) -> None:
    section_heading("CONTENT CALENDAR", "🗓️ 콘텐츠 캘린더", "마감과 배포 일정을 채널별로 확인합니다.")
    if not items:
        st.markdown('<div class="empty-state">일정이 아직 없어요.</div>', unsafe_allow_html=True)
        return
    rows = []
    for item in sorted(items, key=lambda row: row["due_date"]):
        due = datetime.fromisoformat(item["due_date"])
        rows.append({"날짜": due.strftime("%m월 %d일"), "요일": "월화수목금토일"[due.weekday()], "업무": item["title"], "유형": item["type"], "채널": item["channel"], "담당": item["owner"], "상태": item["status"]})
    frame = pd.DataFrame(rows)
    st.dataframe(frame, width="stretch", hide_index=True, height=min(520, 76 + len(frame) * 36))
    st.write("")
    section_heading("CHANNEL BALANCE", "채널별 업무 분포")
    channel_data = frame.assign(채널=frame["채널"].str.split("·")).explode("채널")["채널"].value_counts()
    st.bar_chart(channel_data, horizontal=True, color="#207F82")


def media_page(items: list[dict]) -> None:
    section_heading("MEDIA DESK", "📰 언론·취재 관리", "보도자료, 취재 요청, 기자 접촉 이력을 연결해 관리합니다.")
    c1, c2, c3 = st.columns(3)
    c1.metric("이번 달 보도 노출", "47건", "+12%")
    c2.metric("핵심 메시지 반영", "81%", "+6%p")
    c3.metric("취재 응답 평균", "2.4시간", "SLA 이내")
    st.write("")
    media_items = [row for row in items if row["type"] in {"보도자료", "언론취재"}]
    for item in media_items:
        st.markdown(task_card(item), unsafe_allow_html=True)
        task_controls(item, "media")
    st.info("기자·매체 연락처에는 최근 접촉일, 관심 분야, 선호 연락방식, 약속한 후속자료를 함께 기록하세요.", icon="💌")


def issue_page(items: list[dict]) -> None:
    section_heading("ISSUE ROOM", "🚨 위기·이슈 대응", "확인된 사실과 추정을 분리하고 대외 메시지를 일원화합니다.")
    st.markdown('<div class="warning-panel"><b>대외 답변 전 확인</b><br><small>최초 발견시각 · 사실 원출처 · 책임자 · 법무/관련부서 검토 · 승인된 문안</small></div>', unsafe_allow_html=True)
    issues = [row for row in items if row["type"] == "위기이슈"]
    for item in issues:
        st.markdown(task_card(item), unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(f"**대외 메시지:** {escape(item['key_message'])}")
            st.markdown(f"**핵심 위험:** {escape(item['risk'])}")
            st.markdown(f"**현재 메모:** {escape(item['memo'])}")
        task_controls(item, "issue")
    st.write("")
    steps = ["인지·캡처", "사실확인", "1차 보고", "대응문안", "승인·배포", "모니터링", "회고"]
    step_cols = st.columns(7)
    for index, (column, label) in enumerate(zip(step_cols, steps), start=1):
        column.markdown(f"<div class='soft-panel' style='text-align:center'><b style='color:#207f82'>0{index}</b><br><small>{label}</small></div>", unsafe_allow_html=True)


def performance_page(items: list[dict]) -> None:
    section_heading("OUTCOME, NOT OUTPUT", "📊 홍보 성과", "게시 건수뿐 아니라 메시지 전달과 행동 변화를 함께 봅니다.")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("보도 노출", "47건", "+12%")
    c2.metric("자사채널 도달", "128K", "+18%")
    c3.metric("평균 반응률", "6.8%", "+1.3%p")
    c4.metric("완료 업무", len([row for row in items if row["status"] == "완료"]))
    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        section_heading("SCORE", "커뮤니케이션 품질")
        scores = pd.DataFrame({"항목": ["핵심 메시지 반영률", "긍정·중립 보도 비율", "마감 준수율", "승인 1회 통과율"], "점수": [81, 92, 88, 74]}).set_index("항목")
        st.bar_chart(scores, horizontal=True, color="#207F82")
    with right:
        section_heading("MEASUREMENT", "성과 해석 5단계")
        stages = [("1", "산출", "보도자료·영상·게시물·행사"), ("2", "도달", "노출·조회·도달·기자 접촉"), ("3", "반응", "클릭·공유·문의·톤앤매너"), ("4", "이해", "핵심 메시지 반영·오해 감소"), ("5", "행동", "신청·방문·참여·내부 실행")]
        for number, title, detail in stages:
            st.markdown(f"<div class='soft-panel'><b style='color:#e0a72e'>0{number}</b> &nbsp; <strong>{title}</strong><br><small style='color:#748381'>{detail}</small></div>", unsafe_allow_html=True)


def standards_page() -> None:
    section_heading("STANDARD & LEARNING", "📚 업무 기준과 재발방지", "담당자가 바뀌어도 같은 품질로 일하도록 경험을 자산화합니다.")
    columns = st.columns(3)
    for index, (icon, title, detail) in enumerate(PLAYBOOKS):
        columns[index % 3].markdown(f"<div class='playbook'><div class='emoji'>{icon}</div><h3>{title}</h3><p>{detail}</p><span class='badge'>{len(CHECKLISTS.get(title, [])) or index + 7}개 기준</span></div>", unsafe_allow_html=True)
        if index == 2:
            st.write("")
    st.write("")
    section_heading("LESSONS LEARNED", "실수와 피드백을 다음 기준으로")
    for category, title, detail, rule in LESSONS:
        with st.expander(f"{category} · {title}"):
            st.write(detail)
            st.success(f"다음부터 적용: {rule}", icon="🌱")


render_sidebar_brand()
with st.sidebar:
    st.markdown("---")
    menu = st.radio(
        "업무 메뉴",
        ["오늘", "업무 보드", "콘텐츠 캘린더", "언론·취재", "위기·이슈", "성과", "업무 기준"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    if st.button("＋ 새 업무", type="primary", width="stretch"):
        create_work_dialog()
    st.download_button("⬇ JSON 백업", data=export_json(), file_name=f"pr-flow-{date.today().isoformat()}.json", mime="application/json", width="stretch")
    uploaded = st.file_uploader("백업 불러오기", type=["json"], label_visibility="collapsed")
    if uploaded and st.button("백업 적용", width="stretch"):
        ok, message = import_json(uploaded.getvalue())
        (st.success if ok else st.error)(message)
        if ok:
            st.rerun()
    st.caption("GitHub → Streamlit 자동 배포용 버전")

show_flash()
all_items = st.session_state.work_items

top_left, top_right = st.columns([3, 1])
with top_left:
    search = st.text_input("통합 검색", placeholder="업무명, 담당자, 채널, 핵심 메시지 검색", label_visibility="collapsed")
with top_right:
    type_filter = st.selectbox("유형", ["전체"] + TYPES, label_visibility="collapsed")

filtered_items = all_items
if search:
    query = search.lower().strip()
    filtered_items = [row for row in filtered_items if query in " ".join(str(value) for value in row.values()).lower()]
if type_filter != "전체":
    filtered_items = [row for row in filtered_items if row["type"] == type_filter]

if menu == "오늘":
    dashboard_page(filtered_items)
elif menu == "업무 보드":
    board_page(filtered_items)
elif menu == "콘텐츠 캘린더":
    calendar_page(filtered_items)
elif menu == "언론·취재":
    media_page(filtered_items)
elif menu == "위기·이슈":
    issue_page(filtered_items)
elif menu == "성과":
    performance_page(all_items)
else:
    standards_page()

st.markdown('<div class="foot-note">🌊 홍보 바다 · 기록이 쌓일수록 업무는 가벼워집니다.</div>', unsafe_allow_html=True)
