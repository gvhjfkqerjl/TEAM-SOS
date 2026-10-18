import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="TEAM SOS", layout="wide")

st.markdown("""
<style>
.stApp { background: #FFFFFF; color: #111111; }
.block-container { max-width: 1120px; padding-top: 2.2rem; padding-bottom: 3rem; }
h1, h2, h3, h4, p, label, .stMarkdown { color: #111111; }
.hero { background: #111111; padding: 42px 44px; border-radius: 4px; color: #FFFFFF; margin-bottom: 26px; }
.hero .eyebrow { color: #BDBDBD; font-size: 12px; letter-spacing: 0.22em; font-weight: 700; margin-bottom: 14px; }
.hero-title-row { display: flex; align-items: center; flex-wrap: wrap; gap: 22px; margin: 0 0 14px 0; }
.hero h1 { color: #FFFFFF; font-size: clamp(38px, 5vw, 58px); font-weight: 750; letter-spacing: -0.055em; line-height: 1.05; margin: 0; }
.team-name { color: #E5E5E5; font-size: clamp(18px, 2.1vw, 26px); font-weight: 550; letter-spacing: -0.025em; border-left: 1px solid #777777; padding-left: 22px; line-height: 1.5; }
.hero p { color: #D4D4D4; font-size: 16px; margin: 0; }
.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 1px solid #E4E4E7; }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 0; padding: 12px 16px; color: #666666; font-weight: 600; }
.stTabs [aria-selected="true"] { color: #111111 !important; border-bottom: 2px solid #111111; }
div.stButton > button, div.stFormSubmitButton > button { background: #111111; color: #FFFFFF; border: 1px solid #111111; border-radius: 4px; min-height: 44px; font-weight: 650; transition: all .15s ease; }
div.stButton > button:hover, div.stFormSubmitButton > button:hover { background: #333333; color: #FFFFFF; border-color: #333333; }
div[data-testid="stMetric"] { background: #F5F5F5; border: 1px solid #E5E5E5; border-radius: 4px; padding: 18px; }
div[data-testid="stMetricLabel"] { color: #555555; }
div[data-testid="stMetricValue"] { color: #111111; }
div[data-testid="stVerticalBlockBorderWrapper"] { border-color: #E4E4E7; border-radius: 4px; }
textarea, input { border-radius: 4px !important; }
[data-testid="stFileUploader"] { border: 1px dashed #B8B8B8; border-radius: 4px; padding: 12px; }
hr { border-color: #E4E4E7; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# 문제 유형별 해결책 라이브러리
library = {
"역할 및 업무 분담": {
"keys":["역할","업무","분담","맡은 일","무임승차","책임","안 해","불공평","일을 안"],
"message":"우리 업무가 조금 겹치거나 한쪽에 몰린 것 같아. 해야 할 일과 마감일을 같이 정리하고 각자 맡을 부분을 다시 나눠 볼까?",
"items":[
("업무 다시 나누기","해야 할 일을 작은 단위로 나누고 담당자를 정하세요.","오늘","업무 목록을 만들고 각자 맡을 일을 정해요."),
("업무량 균형 맞추기","업무 개수뿐 아니라 난이도와 예상 시간도 비교하세요.","오늘","각 업무에 걸릴 시간을 적어 한쪽에 일이 몰렸는지 봐요."),
("담당자와 마감일 기록","공유 문서에 업무·담당자·마감일·상태를 기록하세요.","오늘","표를 만들어 모든 팀원이 볼 수 있게 공유해요."),
("중간 목표 만들기","큰 과제를 조사·초안·검토 등 작은 단계로 나누세요.","이번 주","단계별 완료 날짜를 정해요."),
("도움 요청 기준","어려움이 생기면 언제 알릴지 미리 합의하세요.","오늘","마감이 어려워질 것 같으면 미리 알리기로 해요."),
("역할 선호도 확인","각자 잘하거나 배우고 싶은 일을 고려하세요.","오늘","선호 업무와 자신 있는 업무를 물어봐요."),
("업무 인수인계","담당자가 바뀌면 진행 상황과 파일 위치를 전달하세요.","필요할 때","완료한 일과 남은 일을 짧게 정리해요."),
("주간 업무 점검","짧은 점검 시간에 진행 상황과 막힌 부분을 공유하세요.","매주","완료·진행 중·도움 필요 항목을 확인해요."),
("완료 기준 정하기","업무가 언제 완료된 것으로 볼지 미리 정하세요.","오늘","자료 조사라면 출처와 핵심 요약 등 기준을 정해요."),
("업무 회고","끝난 뒤 역할 분담에서 유지하거나 바꿀 점을 정하세요.","마무리","다음 팀플에서 바꿀 점 하나를 기록해요.")
]},
"의사소통": {
"keys":["소통","연락","대화","답장","의사소통","말을 안","공유","공지","읽씹"],
"message":"중요한 내용이 서로 다르게 전달되는 것 같아. 공지와 결정 사항을 한 곳에 모으고, 회의 후 담당 업무를 같이 정리해 볼까?",
"items":[
("공통 채널 정하기","공지와 중요한 결정은 한 곳에 모으세요.","오늘","팀이 자주 확인하는 채팅방이나 문서를 공식 채널로 정해요."),
("응답 시간 합의","즉시 답하기 어려울 수 있으니 답변 기준을 함께 정하세요.","오늘","급한 메시지와 일반 메시지를 구분해요."),
("회의 요약 공유","결정 사항·담당자·마감일을 회의 직후 공유하세요.","매 회의 후","합의한 내용을 메시지로 정리해요."),
("요청을 명확히 쓰기","필요한 행동과 기한을 구체적으로 전달하세요.","오늘","무엇을 언제까지 확인해야 하는지 적어요."),
("정기 체크인","짧은 시간에 진행 상황과 필요한 도움을 공유하세요.","매주","10분 정도 진행 상황을 확인해요."),
("모두에게 발언 기회","회의에서 한 사람씩 의견을 말하도록 해요.","다음 회의","돌아가며 의견과 이유를 말해요."),
("확인 질문하기","추측하지 말고 이해한 내용을 되물어 확인하세요.","필요할 때","제가 이해한 게 맞는지 요약해 확인해요."),
("결정 기록 남기기","결정 내용과 이유를 기록해 혼선을 줄이세요.","결정할 때","공유 문서에 한두 문장으로 남겨요."),
("메시지 우선순위","긴급도 표시 기준을 정해 메시지 중요도를 구분하세요.","오늘","긴급·오늘 확인·참고 표시를 사용해요."),
("상황 중심으로 말하기","비난보다 실제 상황과 필요한 변화를 이야기하세요.","필요할 때","상황과 다음에 필요한 행동을 차분히 말해요.")
]},
"시간 및 일정 관리": {
"keys":["시간","일정","마감","늦","기한","미루","발표 준비","촉박","지연","급해"],
"message":"발표 준비 일정이 촉박해진 것 같아. 남은 일을 정리하고 중간 마감일과 최종 점검 시간을 같이 정해 볼까?",
"items":[
("마감일 역산","제출일에서 거꾸로 계산해 조사·초안·검토 날짜를 정하세요.","오늘","최종 제출 전 내부 마감일을 정해요."),
("중간 마감일 설정","최종 마감 외에 작은 결과물을 확인할 날짜를 정하세요.","오늘","자료 조사와 초안 날짜를 따로 정해요."),
("우선순위 정하기","중요도가 높은 일을 먼저 처리하세요.","오늘","꼭 해야 할 일과 있으면 좋은 일을 나눠요."),
("여유 시간 확보","수정이나 지연을 고려해 일정에 여유를 남겨요.","계획할 때","검토와 수정 시간을 일정에 포함해요."),
("짧은 진행 점검","완료한 일과 막힌 일만 빠르게 확인하세요.","매일 또는 격일","완료·다음 할 일·도움 필요를 한 줄씩 공유해요."),
("작업 시간 추정","업무별 예상 시간을 적고 실제와 비교하세요.","계획할 때","조사와 발표 자료 제작 시간을 각각 추정해요."),
("지연 즉시 공유","마감이 어려워질 것 같으면 늦기 전에 알리세요.","문제 발생 시","지연 이유와 가능한 완료 날짜를 알려요."),
("리허설 예약","자료 제작뿐 아니라 발표 연습 시간도 확보하세요.","발표 전","전체 발표를 이어서 연습해요."),
("공유 일정표","회의와 마감일을 한눈에 보이게 하세요.","오늘","팀원 모두가 볼 수 있는 일정을 만들어요."),
("최종 점검표","파일 형식·출처·제출 위치 등을 마지막에 확인하세요.","제출 전","확인 항목을 나눠 함께 점검해요.")
]},
"의견 충돌": {
"keys":["갈등","싸움","의견","다툼","반대","충돌","결정","고집","불만","기분 나"],
"message":"우리 의견이 다른 것 같아. 서로 중요하게 생각하는 점을 먼저 듣고, 프로젝트 목표에 맞춰 선택지를 비교해 보면 어떨까?",
"items":[
("의견과 이유 구분","무엇을 원하는지뿐 아니라 이유도 들어 보세요.","다음 회의","각 의견의 장점과 우려를 따로 적어요."),
("공통 목표 확인","개인 취향보다 프로젝트 목표와 평가 기준을 중심으로 판단하세요.","오늘","좋은 결과물의 기준을 먼저 합의해요."),
("대안 비교표","선택지의 장점·단점·시간·난이도를 비교하세요.","결정 전","두세 가지 대안을 같은 기준으로 평가해요."),
("모두에게 발언 기회","말이 적은 팀원도 의견을 낼 수 있게 해요.","다음 회의","먼저 각자 의견을 적고 돌아가며 설명해요."),
("사실과 추측 구분","상대의 의도를 추측하지 말고 실제 상황을 확인하세요.","갈등 발생 시","관찰한 사실과 추측을 구분해 말해요."),
("임시 결정 후 검토","시간이 부족하면 임시안을 정하고 다시 평가하세요.","급할 때","초안을 선택하고 다음 날 기준에 맞는지 확인해요."),
("중립 진행자","논의가 반복되면 중립적인 사람이 순서를 도울 수 있어요.","필요할 때","서로의 말을 요약하고 결론을 강요하지 않아요."),
("합의 규칙 정하기","만장일치인지 다수결인지 결정 규칙을 미리 정하세요.","프로젝트 초반","의견이 갈릴 때 적용할 규칙을 합의해요."),
("잠시 쉬고 다시 논의","감정이 격해졌다면 쉬었다가 차분히 다시 이야기하세요.","필요할 때","휴식 후 해결할 문제 하나에 집중해요."),
("문제에 집중하기","누가 잘못했는지보다 바꿀 수 있는 행동을 논의하세요.","갈등 발생 시","비난보다 다음에 필요한 행동을 구체적으로 말해요.")
]}
}

def classify(text):
    scores = {name: sum(k in text.lower() for k in data["keys"]) for name, data in library.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else None

st.markdown("""
<div class="hero">
<p class="eyebrow">TEAMWORK / PROBLEM SOLVING</p>
<div class="hero-title-row">
<h1>TEAM SOS</h1>
<span class="team-name">차이차박</span>
</div>
<p>팀 프로젝트의 문제를 진단하고, 더 나은 협업 방법을 찾아보세요.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["고민 분석", "팀플 위험도 진단", "팀플 통계", "프로젝트 소개"])

with tab1:
    st.subheader("지금 어떤 고민이 있나요?")
    st.write("상황을 입력하면 문제 유형과 실행 가능한 해결 방법을 추천해요.")
    problem = st.text_area("고민 내용", placeholder="예: 팀원이 맡은 일을 늦게 해서 발표 준비가 밀리고 있어요.", height=130)
    number = st.slider("추천받을 해결 방법 개수", 3, 8, 5)
    if st.button("고민 분석하기", use_container_width=True):
        if not problem.strip():
            st.warning("고민 내용을 먼저 입력해 주세요.")
        else:
            category = classify(problem)
            if category is None:
                st.info("유형을 명확히 분류하기 어려워요. 역할 분담, 소통, 일정, 의견 충돌 중 어떤 상황인지 더 자세히 적어 주세요.")
            else:
                st.success(f"예상 문제 유형: {category}")
                st.caption("현재는 키워드 기반 시제품입니다. 학습형 AI 모델의 판단은 아닙니다.")
                items = library[category]["items"]
                words = [w for w in problem.lower().split() if len(w) > 1]
                ranked = sorted(items, key=lambda item: sum(w in (item[0] + item[1] + item[3]).lower() for w in words), reverse=True)
                top = ranked[:min(3, number)]
                rest = [item for item in items if item not in top]
                chosen = top + random.sample(rest, min(number-len(top), len(rest)))
                st.markdown("###  추천 해결 방법")
                for i, (title, desc, when, action) in enumerate(chosen, 1):
                    with st.container(border=True):
                        st.markdown(f"**{i}. {title}**")
                        st.write(desc)
                        st.caption(f"실행 시점: {when}")
                        st.info(f"실행 예시: {action}")
                st.markdown("###  팀원에게 이렇게 말해 보세요")
                st.write(library[category]["message"])
                st.caption("추천은 참고용입니다. 팀 상황에 맞게 조정하세요.")

with tab2:
    st.subheader("우리 팀의 협업 상태를 확인해 보세요")
    st.write("아래 항목은 팀원들과 상의해 현재 상태에 가장 가까운 답을 선택하세요. 이 진단은 평가나 낙인이 아닌, 개선할 부분을 찾기 위한 참고용입니다.")

    with st.form("team_health_form"):
        st.markdown("#### 1. 역할 분담")
        role = st.radio("각자 맡은 일과 마감일이 명확한가요?", [
            "잘 정해져 있고 모두 알고 있어요",
            "대체로 정해졌지만 일부 불명확해요",
            "역할이 겹치거나 누가 할지 불분명해요"
        ], index=0)
        st.markdown("#### 2. 의사소통")
        communication = st.radio("중요한 결정과 진행 상황이 팀원 모두에게 공유되나요?", [
            "잘 공유되고 있어요",
            "가끔 전달이 빠지거나 늦어요",
            "정보가 자주 누락되거나 서로 다르게 알고 있어요"
        ], index=0)
        st.markdown("#### 3. 일정 관리")
        schedule = st.radio("현재 일정과 마감일을 지킬 수 있을 것 같나요?", [
            "계획대로 진행되고 있어요",
            "일부 지연이 있지만 조정할 수 있어요",
            "중요한 일이 밀려 마감이 걱정돼요"
        ], index=0)
        st.markdown("#### 4. 의견 조율")
        conflict = st.radio("의견이 다를 때 서로 말하고 결정을 내릴 수 있나요?", [
            "서로 의견을 듣고 결정해요",
            "결정에 시간이 걸리지만 대화는 가능해요",
            "의견 충돌이 반복되거나 일부 의견이 무시돼요"
        ], index=0)
        submitted = st.form_submit_button("우리 팀 진단하기", use_container_width=True)

    if submitted:
        answers = [
            ("역할 분담", role, ["잘 정해져 있고", "대체로 정해졌지만", "역할이 겹치거나"]),
            ("의사소통", communication, ["잘 공유되고", "가끔 전달이", "정보가 자주"]),
            ("일정 관리", schedule, ["계획대로", "일부 지연이", "중요한 일이"]),
            ("의견 조율", conflict, ["서로 의견을", "결정에 시간이", "의견 충돌이"])
        ]
        risk = 0
        risks = []
        for name, answer, markers in answers:
            level = 0 if answer == answers[0][1] and name == "역할 분담" else 0
            # 각 질문의 답변 순서로 점수 부여
            options = {
                "역할 분담": ["잘 정해져 있고 모두 알고 있어요", "대체로 정해졌지만 일부 불명확해요", "역할이 겹치거나 누가 할지 불분명해요"],
                "의사소통": ["잘 공유되고 있어요", "가끔 전달이 빠지거나 늦어요", "정보가 자주 누락되거나 서로 다르게 알고 있어요"],
                "일정 관리": ["계획대로 진행되고 있어요", "일부 지연이 있지만 조정할 수 있어요", "중요한 일이 밀려 마감이 걱정돼요"],
                "의견 조율": ["서로 의견을 듣고 결정해요", "결정에 시간이 걸리지만 대화는 가능해요", "의견 충돌이 반복되거나 일부 의견이 무시돼요"]
            }
            score = options[name].index(answer)
            risk += score
            if score == 1:
                risks.append((name, "주의", "팀원끼리 짧게 상황을 확인하고 작은 개선 약속을 정해 보세요."))
            elif score == 2:
                risks.append((name, "우선 개선", {
                    "역할 분담": "해야 할 일·담당자·마감일을 한 표에 정리하고 업무량을 다시 나눠 보세요.",
                    "의사소통": "중요한 공지 채널을 하나로 정하고 결정 사항을 글로 남기세요.",
                    "일정 관리": "남은 일을 우선순위별로 정리하고 내부 마감일과 도움 요청 시점을 정하세요.",
                    "의견 조율": "각자 의견과 이유를 듣고 공통 목표에 맞춰 선택지를 비교하세요."
                }[name]))
        st.markdown("###  진단 결과")
        if risk <= 2:
            st.success(f"협업 상태: 양호 — {risk}/8점")
            st.write("현재 기본적인 협업 체계가 잡혀 있는 편이에요. 잘 되는 방식을 유지하면서 중간 점검을 계속해 보세요.")
        elif risk <= 5:
            st.warning(f"협업 상태: 점검 필요 — {risk}/8점")
            st.write("몇 가지 부분을 조금씩 개선하면 팀 프로젝트 진행이 더 안정적일 수 있어요.")
        else:
            st.error(f"협업 상태: 우선 개선 필요 — {risk}/8점")
            st.write("여러 부분에서 어려움이 나타나고 있어요. 팀원들과 짧은 회의를 열어 가장 급한 문제부터 정리해 보세요.")
        st.markdown("### ️ 먼저 개선할 항목")
        if not risks:
            st.write("뚜렷한 위험 항목이 없어요. 현재 협업 방식을 유지하고 정기적으로 확인해 보세요.")
        else:
            for name, label, advice in risks:
                with st.container(border=True):
                    st.markdown(f"**{name} · {label}**")
                    st.write(advice)
        st.caption("이 점수는 자체 점검용이며 과학적으로 검증된 평가나 예측 점수가 아닙니다. 팀원들과 대화를 시작하는 참고 자료로 활용하세요.")

with tab3:
    st.subheader("팀플 문제 데이터 분석")
    st.write("기존 CSV 분석 결과를 업로드해 통계를 확인하세요.")
    uploaded = st.file_uploader("분석 결과 CSV 선택", type=["csv"])
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded, encoding="utf-8-sig")
            df.columns = df.columns.astype(str).str.strip()
            if {"문제유형", "언급 팀 수"}.issubset(df.columns):
                chart = df[["문제유형", "언급 팀 수"]].copy()
                chart["언급 팀 수"] = pd.to_numeric(chart["언급 팀 수"], errors="coerce")
                chart = chart.dropna()
            elif "문제 유형" in df.columns:
                rows = [cat for val in df["문제 유형"].dropna() for cat in str(val).split(", ") if cat != "미분류"]
                chart = pd.Series(rows).value_counts().rename_axis("문제유형").reset_index(name="언급 팀 수")
            else:
                chart = pd.DataFrame()
            if chart.empty:
                st.warning("문제 유형을 찾지 못했어요. 분석 결과 CSV 파일인지 확인해 주세요.")
                st.write("현재 컬럼:", df.columns.tolist())
            else:
                chart = chart.sort_values("언급 팀 수", ascending=False)
                a, b = st.columns(2)
                a.metric("분석된 문제 유형", len(chart))
                b.metric("총 언급 수", int(chart["언급 팀 수"].sum()))
                st.bar_chart(chart.set_index("문제유형")["언급 팀 수"], horizontal=True)
                st.dataframe(chart, use_container_width=True)
        except Exception as e:
            st.error(f"CSV를 읽는 중 문제가 발생했어요: {e}")
    else:
        st.info("CSV 파일을 업로드하면 실제 분석 결과가 여기에 표시돼요.")

with tab4:
    st.subheader("왜 TEAM SOS를 만들었을까요?")
    st.write("팀 프로젝트의 역할 분담, 의사소통, 일정 관리, 의견 충돌 문제를 더 잘 해결하도록 돕는 시제품입니다.")
    st.markdown("""
- **문제 발견:** 팀플 어려움을 데이터로 살펴보기
- **문제 분석:** 입력한 고민을 관련 유형으로 분류하기
- **해결 지원:** 여러 실행 방법과 대화 예시 제공하기
- **협업 진단:** 역할·소통·일정·의견 조율 상태를 자체 점검하기
- **향후 개선:** 실제 학생 테스트와 학습형 AI 모델 개발
""")

st.divider()
st.caption("TEAM SOS · 팀플을 더 나은 협업 경험으로")
