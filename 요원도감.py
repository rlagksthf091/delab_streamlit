import html
import json
from urllib.error import URLError
from urllib.request import urlopen

import streamlit as st


PATCH_DATE = "2026-07-07"
API_URL = "https://valorant-api.com/v1/agents?isPlayableCharacter=true&language=ko-KR"

ROLE_META = {
    "Duelist": {
        "ko": "타격대",
        "icon": "D",
        "color": "#ff4655",
        "summary": "교전을 열고 진입 각을 만드는 전방 압박 요원",
    },
    "Initiator": {
        "ko": "척후대",
        "icon": "I",
        "color": "#f0b65a",
        "summary": "정보 수집과 교전 개시로 팀의 진입을 돕는 요원",
    },
    "Controller": {
        "ko": "전략가",
        "icon": "C",
        "color": "#43d6a4",
        "summary": "시야 차단과 공간 분리로 전장을 설계하는 요원",
    },
    "Sentinel": {
        "ko": "감시자",
        "icon": "S",
        "color": "#62a8ff",
        "summary": "거점 방어, 후방 감시, 재진입 차단에 특화된 요원",
    },
}

ORIGINS = {
    "Astra": "가나",
    "Breach": "스웨덴",
    "Brimstone": "미국",
    "Chamber": "프랑스",
    "Clove": "스코틀랜드",
    "Cypher": "모로코",
    "Deadlock": "노르웨이",
    "Fade": "튀르키예",
    "Gekko": "미국",
    "Harbor": "인도",
    "Iso": "중국",
    "Jett": "대한민국",
    "KAY/O": "기원 불명",
    "Killjoy": "독일",
    "Miks": "크로아티아",
    "Neon": "필리핀",
    "Omen": "기원 불명",
    "Phoenix": "영국",
    "Raze": "브라질",
    "Reyna": "멕시코",
    "Sage": "중국",
    "Skye": "호주",
    "Sova": "러시아",
    "Tejo": "콜롬비아",
    "Veto": "세네갈",
    "Viper": "미국",
    "Vyse": "기원 불명",
    "Waylay": "태국",
    "Yoru": "일본",
}

FALLBACK_AGENTS = [
    {"displayName": "Astra", "displayIcon": "", "fullPortrait": "", "description": "가나 출신 전략가. 별의 힘으로 전장을 원격 제어합니다.", "role": {"displayName": "전략가", "developerName": "Controller"}, "abilities": []},
    {"displayName": "Breach", "displayIcon": "", "fullPortrait": "", "description": "스웨덴 출신 척후대. 벽 너머로 강력한 충격을 전달합니다.", "role": {"displayName": "척후대", "developerName": "Initiator"}, "abilities": []},
    {"displayName": "Brimstone", "displayIcon": "", "fullPortrait": "", "description": "미국 출신 전략가. 궤도 지원과 연막으로 팀을 지휘합니다.", "role": {"displayName": "전략가", "developerName": "Controller"}, "abilities": []},
    {"displayName": "Chamber", "displayIcon": "", "fullPortrait": "", "description": "프랑스 출신 감시자. 정밀한 무기와 함정으로 각을 장악합니다.", "role": {"displayName": "감시자", "developerName": "Sentinel"}, "abilities": []},
    {"displayName": "Clove", "displayIcon": "", "fullPortrait": "", "description": "스코틀랜드 출신 전략가. 사망 이후에도 전장에 영향력을 남깁니다.", "role": {"displayName": "전략가", "developerName": "Controller"}, "abilities": []},
    {"displayName": "Cypher", "displayIcon": "", "fullPortrait": "", "description": "모로코 출신 감시자. 감시 장비로 적의 움직임을 추적합니다.", "role": {"displayName": "감시자", "developerName": "Sentinel"}, "abilities": []},
    {"displayName": "Deadlock", "displayIcon": "", "fullPortrait": "", "description": "노르웨이 출신 감시자. 나노와이어 장비로 진입을 묶어냅니다.", "role": {"displayName": "감시자", "developerName": "Sentinel"}, "abilities": []},
    {"displayName": "Fade", "displayIcon": "", "fullPortrait": "", "description": "튀르키예 출신 척후대. 공포와 추적으로 적의 위치를 드러냅니다.", "role": {"displayName": "척후대", "developerName": "Initiator"}, "abilities": []},
    {"displayName": "Gekko", "displayIcon": "", "fullPortrait": "", "description": "미국 로스앤젤레스 출신 척후대. 동료 생명체들과 함께 교전을 엽니다.", "role": {"displayName": "척후대", "developerName": "Initiator"}, "abilities": []},
    {"displayName": "Harbor", "displayIcon": "", "fullPortrait": "", "description": "인도 출신 전략가. 물의 벽과 방패로 시야와 진입로를 조절합니다.", "role": {"displayName": "전략가", "developerName": "Controller"}, "abilities": []},
    {"displayName": "Iso", "displayIcon": "", "fullPortrait": "", "description": "중국 출신 타격대. 보호막과 결투 구도로 1대1을 강제합니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
    {"displayName": "Jett", "displayIcon": "", "fullPortrait": "", "description": "대한민국 출신 타격대. 빠른 기동성과 회피로 공간을 엽니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
    {"displayName": "KAY/O", "displayIcon": "", "fullPortrait": "", "description": "미래에서 온 척후대. 적의 스킬 사용을 억제합니다.", "role": {"displayName": "척후대", "developerName": "Initiator"}, "abilities": []},
    {"displayName": "Killjoy", "displayIcon": "", "fullPortrait": "", "description": "독일 출신 감시자. 자동 장비로 지역을 봉쇄합니다.", "role": {"displayName": "감시자", "developerName": "Sentinel"}, "abilities": []},
    {"displayName": "Miks", "displayIcon": "", "fullPortrait": "", "description": "크로아티아 출신 전략가. 소리 에너지로 팀의 템포를 맞추고 전장을 흔듭니다.", "role": {"displayName": "전략가", "developerName": "Controller"}, "abilities": []},
    {"displayName": "Neon", "displayIcon": "", "fullPortrait": "", "description": "필리핀 출신 타격대. 전기 에너지와 속도로 적진을 돌파합니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
    {"displayName": "Omen", "displayIcon": "", "fullPortrait": "", "description": "기원 불명의 전략가. 어둠과 순간이동으로 시야를 흔듭니다.", "role": {"displayName": "전략가", "developerName": "Controller"}, "abilities": []},
    {"displayName": "Phoenix", "displayIcon": "", "fullPortrait": "", "description": "영국 출신 타격대. 불꽃으로 공격과 회복을 동시에 수행합니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
    {"displayName": "Raze", "displayIcon": "", "fullPortrait": "", "description": "브라질 출신 타격대. 폭발물로 좁은 공간을 강제로 비웁니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
    {"displayName": "Reyna", "displayIcon": "", "fullPortrait": "", "description": "멕시코 출신 타격대. 처치 이후 회복과 회피로 연속 교전을 노립니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
    {"displayName": "Sage", "displayIcon": "", "fullPortrait": "", "description": "중국 출신 감시자. 회복과 장벽으로 팀의 생존을 책임집니다.", "role": {"displayName": "감시자", "developerName": "Sentinel"}, "abilities": []},
    {"displayName": "Skye", "displayIcon": "", "fullPortrait": "", "description": "호주 출신 척후대. 정령을 보내 정찰, 섬광, 회복을 지원합니다.", "role": {"displayName": "척후대", "developerName": "Initiator"}, "abilities": []},
    {"displayName": "Sova", "displayIcon": "", "fullPortrait": "", "description": "러시아 출신 척후대. 정찰 화살과 드론으로 정보를 확보합니다.", "role": {"displayName": "척후대", "developerName": "Initiator"}, "abilities": []},
    {"displayName": "Tejo", "displayIcon": "", "fullPortrait": "", "description": "콜롬비아 출신 척후대. 드론과 유도 타격으로 적을 몰아냅니다.", "role": {"displayName": "척후대", "developerName": "Initiator"}, "abilities": []},
    {"displayName": "Veto", "displayIcon": "", "fullPortrait": "", "description": "세네갈 출신 감시자. 변이 능력으로 적 유틸리티와 진입을 무력화합니다.", "role": {"displayName": "감시자", "developerName": "Sentinel"}, "abilities": []},
    {"displayName": "Viper", "displayIcon": "", "fullPortrait": "", "description": "미국 출신 전략가. 독성 장막과 구름으로 영역을 잠식합니다.", "role": {"displayName": "전략가", "developerName": "Controller"}, "abilities": []},
    {"displayName": "Vyse", "displayIcon": "", "fullPortrait": "", "description": "기원 불명의 감시자. 액체 금속으로 적을 고립시키고 무장을 방해합니다.", "role": {"displayName": "감시자", "developerName": "Sentinel"}, "abilities": []},
    {"displayName": "Waylay", "displayIcon": "", "fullPortrait": "", "description": "태국 출신 타격대. 빛으로 돌진하고 되돌아오며 적을 둔화시킵니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
    {"displayName": "Yoru", "displayIcon": "", "fullPortrait": "", "description": "일본 출신 타격대. 차원 이동과 기만으로 뒤를 잡습니다.", "role": {"displayName": "타격대", "developerName": "Duelist"}, "abilities": []},
]


def esc(value):
    return html.escape(str(value or ""), quote=True)


@st.cache_data(ttl=60 * 60 * 6, show_spinner=False)
def load_agents():
    try:
        with urlopen(API_URL, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))
        agents = payload.get("data", [])
        if agents:
            return sorted(agents, key=lambda item: item.get("displayName", "")), True
    except (URLError, TimeoutError, ValueError, OSError):
        pass
    return sorted(FALLBACK_AGENTS, key=lambda item: item.get("displayName", "")), False


def role_key(agent):
    role = agent.get("role") or {}
    developer_name = role.get("developerName") or ""
    if developer_name in ROLE_META:
        return developer_name

    ko_name = role.get("displayName") or ""
    for key, meta in ROLE_META.items():
        if meta["ko"] == ko_name:
            return key
    return "Duelist"


def agent_slug(agent):
    return (agent.get("developerName") or agent.get("displayName") or "").lower().replace("/", "").replace(" ", "-")


def ability_slots(abilities):
    labels = ["C", "Q", "E", "X"]
    cleaned = [ability for ability in abilities or [] if ability.get("displayName")]
    for index, ability in enumerate(cleaned[:4]):
        yield labels[index], ability


st.set_page_config(page_title="VALORANT 요원 도감", page_icon="V", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Rajdhani:wght@600;700&display=swap');

:root {
  --bg: #07111f;
  --panel: #0d1b2e;
  --panel-2: #10243c;
  --line: #203755;
  --text: #ece8e1;
  --muted: #91a4b7;
  --riot: #ff4655;
}

.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
  background: radial-gradient(circle at 20% 0%, #182d45 0, #07111f 34rem);
  color: var(--text);
  font-family: 'Noto Sans KR', sans-serif;
}

[data-testid="stHeader"] {
  background: rgba(7, 17, 31, .86);
  backdrop-filter: blur(10px);
}

.block-container {
  padding-top: 2rem;
  padding-bottom: 3rem;
}

div.stButton > button {
  border-radius: 6px;
  border: 1px solid var(--line);
  background: #0d1b2e;
  color: var(--text);
  font-weight: 700;
  min-height: 2.65rem;
}

div.stButton > button:hover {
  border-color: var(--riot);
  color: #fff;
  background: #13243a;
}

.hero {
  border-bottom: 1px solid var(--line);
  padding: .6rem 0 1.4rem;
  margin-bottom: 1.1rem;
}

.brand {
  font-family: 'Rajdhani', sans-serif;
  font-size: clamp(2.2rem, 5vw, 5.4rem);
  line-height: .88;
  letter-spacing: 0;
  font-weight: 700;
}

.brand span {
  color: var(--riot);
}

.subline {
  color: var(--muted);
  margin-top: .85rem;
  max-width: 62rem;
  line-height: 1.65;
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: .65rem;
  margin: 1rem 0 1.2rem;
}

.metric {
  border: 1px solid var(--line);
  background: rgba(13, 27, 46, .86);
  border-radius: 8px;
  padding: .9rem 1rem;
}

.metric .num {
  font-family: 'Rajdhani', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
}

.metric .label {
  color: var(--muted);
  font-size: .85rem;
  margin-top: .25rem;
}

.agent-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: linear-gradient(180deg, rgba(16, 36, 60, .95), rgba(9, 20, 36, .95));
  min-height: 18.5rem;
  padding: .85rem;
  overflow: hidden;
  position: relative;
}

.agent-card.selected {
  border-color: var(--riot);
  box-shadow: 0 0 0 1px rgba(255, 70, 85, .3) inset;
}

.portrait-wrap {
  height: 10.5rem;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  background: linear-gradient(135deg, rgba(255,70,85,.16), rgba(98,168,255,.12));
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 6px;
  overflow: hidden;
}

.portrait-wrap img {
  max-width: 115%;
  max-height: 13.5rem;
  object-fit: contain;
}

.portrait-fallback {
  font-family: 'Rajdhani', sans-serif;
  font-size: 4.5rem;
  font-weight: 700;
  color: rgba(236, 232, 225, .28);
}

.agent-name {
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  margin-top: .75rem;
  line-height: 1;
}

.agent-meta {
  color: var(--muted);
  font-size: .86rem;
  margin-top: .35rem;
}

.role-pill {
  display: inline-flex;
  align-items: center;
  gap: .4rem;
  border: 1px solid currentColor;
  border-radius: 999px;
  padding: .18rem .55rem;
  font-size: .78rem;
  font-weight: 700;
}

.detail {
  border: 1px solid var(--riot);
  border-radius: 8px;
  background: rgba(9, 20, 36, .94);
  overflow: hidden;
  margin-bottom: 1.25rem;
}

.detail-inner {
  display: grid;
  grid-template-columns: minmax(15rem, 24rem) 1fr;
  gap: 1rem;
  padding: 1rem;
}

.detail-art {
  min-height: 24rem;
  border-radius: 6px;
  background: linear-gradient(150deg, rgba(255,70,85,.24), rgba(67,214,164,.12));
  display: flex;
  align-items: flex-end;
  justify-content: center;
  overflow: hidden;
}

.detail-art img {
  width: 120%;
  max-height: 31rem;
  object-fit: contain;
}

.detail-title {
  font-family: 'Rajdhani', sans-serif;
  font-size: clamp(2.4rem, 6vw, 5rem);
  line-height: .9;
  font-weight: 700;
}

.description {
  color: #bdc8d3;
  line-height: 1.75;
  margin: .85rem 0 1rem;
}

.ability {
  display: grid;
  grid-template-columns: 3.25rem 1fr;
  gap: .85rem;
  padding: .9rem 0;
  border-top: 1px solid var(--line);
}

.key {
  width: 3.25rem;
  height: 3.25rem;
  border-radius: 6px;
  border: 1px solid var(--line);
  background: #07111f;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Rajdhani', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--riot);
}

.ability-name {
  font-weight: 900;
  margin-bottom: .25rem;
}

.ability-desc {
  color: var(--muted);
  line-height: 1.6;
  font-size: .94rem;
}

.source-note {
  color: var(--muted);
  font-size: .86rem;
  border-top: 1px solid var(--line);
  margin-top: 1.5rem;
  padding-top: 1rem;
}

@media (max-width: 900px) {
  .metric-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .detail-inner {
    grid-template-columns: 1fr;
  }
  .detail-art {
    min-height: 18rem;
  }
}
</style>
""",
    unsafe_allow_html=True,
)

agents, from_api = load_agents()

if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = "Miks" if any(a.get("displayName") == "Miks" for a in agents) else agents[0]["displayName"]

st.markdown(
    f"""
<section class="hero">
  <div class="brand"><span>VALORANT</span><br>요원 도감</div>
</section>
""",
    unsafe_allow_html=True,
)

counts = {key: 0 for key in ROLE_META}
for item in agents:
    counts[role_key(item)] += 1

metric_html = [f'<div class="metric"><div class="num">{len(agents)}</div><div class="label">전체 요원</div></div>']
for key, meta in ROLE_META.items():
    metric_html.append(
        f'<div class="metric"><div class="num" style="color:{meta["color"]}">{counts[key]}</div>'
        f'<div class="label">{meta["ko"]}</div></div>'
    )
st.markdown(f'<div class="metric-grid">{"".join(metric_html)}</div>', unsafe_allow_html=True)

left, right = st.columns([1.1, 2.2], gap="large")

with left:
    search = st.text_input("요원 검색", placeholder="예: 제트, Jett, 감시자", label_visibility="collapsed")
    selected_role = st.segmented_control(
        "역할 필터",
        ["전체", "타격대", "척후대", "전략가", "감시자"],
        default="전체",
        label_visibility="collapsed",
    )

    def matches_filter(agent):
        role = ROLE_META[role_key(agent)]["ko"]
        origin = ORIGINS.get(agent.get("displayName"), "정보 없음")
        haystack = " ".join([agent.get("displayName", ""), role, origin, agent.get("description", "")]).lower()
        role_ok = selected_role == "전체" or role == selected_role
        search_ok = not search or search.lower().strip() in haystack
        return role_ok and search_ok

    visible_agents = [agent for agent in agents if matches_filter(agent)]
    st.caption(f"{len(visible_agents)}명 표시 중")

    for index in range(0, len(visible_agents), 2):
        cols = st.columns(2)
        for col, agent in zip(cols, visible_agents[index:index + 2]):
            name = agent.get("displayName", "")
            role = ROLE_META[role_key(agent)]
            origin = ORIGINS.get(name, "정보 없음")
            icon = agent.get("fullPortrait") or agent.get("displayIcon") or ""
            selected_class = " selected" if st.session_state.selected_agent == name else ""
            image_html = (
                f'<img src="{esc(icon)}" alt="{esc(name)}">'
                if icon
                else f'<div class="portrait-fallback">{esc(name[:1])}</div>'
            )
            with col:
                st.markdown(
                    f"""
<div class="agent-card{selected_class}">
  <div class="portrait-wrap">{image_html}</div>
  <div class="agent-name">{esc(name)}</div>
  <div class="agent-meta">{esc(origin)}</div>
  <div style="margin-top:.55rem;color:{role["color"]}">
    <span class="role-pill">{role["icon"]} {role["ko"]}</span>
  </div>
</div>
""",
                    unsafe_allow_html=True,
                )
                if st.button("선택", key=f"pick_{agent_slug(agent)}", use_container_width=True):
                    st.session_state.selected_agent = name
                    st.rerun()

with right:
    selected = next((agent for agent in agents if agent.get("displayName") == st.session_state.selected_agent), agents[0])
    name = selected.get("displayName", "")
    role = ROLE_META[role_key(selected)]
    origin = ORIGINS.get(name, "정보 없음")
    portrait = selected.get("fullPortrait") or selected.get("displayIcon") or ""
    portrait_html = (
        f'<img src="{esc(portrait)}" alt="{esc(name)}">'
        if portrait
        else f'<div class="portrait-fallback">{esc(name[:1])}</div>'
    )

    ability_html = []
    for key_label, ability in ability_slots(selected.get("abilities")):
        ability_html.append(
            f"""
<div class="ability">
  <div class="key">{esc(key_label)}</div>
  <div>
    <div class="ability-name">{esc(ability.get("displayName"))}</div>
    <div class="ability-desc">{esc(ability.get("description") or "API에서 세부 설명을 불러오지 못했습니다.")}</div>
  </div>
</div>
"""
        )
    if not ability_html:
        ability_html.append(
            """
<div class="ability">
  <div class="key">!</div>
  <div>
    <div class="ability-name">오프라인 기본 정보</div>
    <div class="ability-desc">네트워크 연결이 복구되면 한국어 스킬 설명과 초상화가 자동으로 표시됩니다.</div>
  </div>
</div>
"""
        )

    st.markdown(
        f"""
<div class="detail">
  <div class="detail-inner">
    <div class="detail-art">{portrait_html}</div>
    <div>
      <div style="color:{role["color"]}; margin-bottom:.75rem;">
        <span class="role-pill">{role["icon"]} {role["ko"]}</span>
      </div>
      <div class="detail-title">{esc(name)}</div>
      <div class="agent-meta">출신: {esc(origin)} · 역할: {esc(role["summary"])}</div>
      <div class="description">{esc(selected.get("description") or "요원 설명을 불러오지 못했습니다.")}</div>
      {"".join(ability_html)}
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

data_state = "한국어 API 연결됨" if from_api else "오프라인 fallback 사용 중"
st.markdown(
    f"""
<div class="source-note">
  데이터 상태: {data_state}. 공식 VALORANT 요원 페이지와 valorant-api 한국어 데이터를 기준으로 구성했습니다.
</div>
""",
    unsafe_allow_html=True,
)
