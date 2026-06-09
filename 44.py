import streamlit as st

st.set_page_config(page_title="VALORANT 요원 도감", page_icon="🎯", layout="wide")

# ── 스타일 ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] { font-family: 'Rajdhani', sans-serif; }

.val-header {
    display: flex; align-items: center; gap: 16px;
    border-bottom: 1px solid #1e3040; padding-bottom: 1.25rem; margin-bottom: 1.5rem;
}
.val-logo { font-size: 28px; font-weight: 700; letter-spacing: 4px; color: #ff4655; text-transform: uppercase; }
.val-logo span { color: #ece8e1; }
.val-subtitle { font-size: 12px; letter-spacing: 2px; color: #7a8c99; font-family: 'Share Tech Mono', monospace; margin-top: 4px; }

.agent-card {
    background: #162028; border: 1px solid #1e3040; border-radius: 2px;
    padding: 14px; cursor: pointer; transition: all .2s;
    margin-bottom: 8px;
}
.agent-card:hover { border-color: #ff4655; }
.agent-card-selected { border-color: #ff4655 !important; background: #1a2535 !important; }

.card-name { font-size: 17px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #ece8e1; }
.card-role { font-size: 11px; color: #7a8c99; letter-spacing: 1.5px; font-family: 'Share Tech Mono', monospace; }
.card-origin { font-size: 11px; color: #7a8c99; margin-top: 6px; }

.detail-panel {
    background: #162028; border: 1px solid #ff4655; border-radius: 2px;
    padding: 24px; margin-bottom: 1.5rem;
}
.detail-name { font-size: 30px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #ece8e1; }
.detail-role { font-size: 13px; color: #7a8c99; letter-spacing: 2px; font-family: 'Share Tech Mono', monospace; margin-top: 4px; }
.detail-desc {
    font-size: 13px; color: #7a8c99; line-height: 1.65;
    padding: 14px; background: #1f2731;
    border-left: 3px solid #ff4655; margin: 16px 0;
}
.ability-row {
    display: grid; grid-template-columns: 60px 1fr auto;
    gap: 14px; align-items: start;
    padding: 12px 0; border-bottom: 1px solid #1e3040;
}
.ability-key {
    width: 52px; height: 52px; background: #1f2731;
    border: 1px solid #1e3040;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center; border-radius: 2px;
}
.key-label { font-size: 18px; font-weight: 700; color: #ff4655; font-family: 'Share Tech Mono', monospace; }
.key-sub { font-size: 9px; color: #7a8c99; letter-spacing: .5px; }
.ability-name { font-size: 15px; font-weight: 700; letter-spacing: .5px; text-transform: uppercase; color: #ece8e1; }
.ability-desc { font-size: 12px; color: #7a8c99; line-height: 1.5; margin-top: 3px; }
.ability-tag {
    display: inline-block; padding: 2px 8px; font-size: 10px;
    letter-spacing: 1px; font-family: 'Share Tech Mono', monospace;
    border-radius: 2px; margin-top: 5px;
}
.dur-val { font-size: 14px; font-weight: 700; color: #ff4655; font-family: 'Share Tech Mono', monospace; white-space: nowrap; }
.dur-label { font-size: 9px; color: #7a8c99; letter-spacing: 1px; white-space: nowrap; }
.abilities-title { font-size: 11px; letter-spacing: 2px; color: #7a8c99; font-family: 'Share Tech Mono', monospace; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 ───────────────────────────────────────────────────────────────────
ROLES = {
    "Duelist":    {"label": "결투사", "icon": "⚔️",  "color": "#ff4655"},
    "Initiator":  {"label": "개시자", "icon": "🔍",  "color": "#e8b86d"},
    "Controller": {"label": "조종사", "icon": "💨",  "color": "#7bc67e"},
    "Sentinel":   {"label": "감시자", "icon": "🛡️", "color": "#5b9bd5"},
}

TYPE_COLORS = {
    "smoke": "#7bc67e", "movement": "#5b9bd5", "flash": "#e8b86d",
    "heal": "#7bc67e",  "damage": "#ff4655",   "ultimate": "#ff4655",
    "recon": "#e8b86d", "debuff": "#c47be8",   "wall": "#7bc67e",
    "buff": "#7bc67e",  "stun": "#e8b86d",     "suppress": "#c47be8",
    "trap": "#e8b86d",  "decoy": "#c47be8",
}

AGENTS = [
    {"id": "jett",      "name": "제트",   "role": "Duelist",    "origin": "대한민국",
     "desc": "칼날처럼 빠른 대한민국 출신 결투사. 바람을 자유자재로 다루며 전장을 누빈다.",
     "abilities": [
         {"key":"C","name":"클라우드버스트","desc":"짧은 연기 수류탄을 던진다. 버튼을 누른 채 곡선 경로를 조정 가능.","duration":"4.5초","type":"smoke"},
         {"key":"Q","name":"업드래프트","desc":"강력한 상승 기류를 일으켜 수직으로 높이 도약한다.","duration":"즉시","type":"movement"},
         {"key":"E","name":"테일윈드","desc":"이동 방향으로 빠르게 돌진한다. 킬 시 즉시 초기화.","duration":"즉시","type":"movement"},
         {"key":"X","name":"블레이드스톰","desc":"정밀 단검을 무한 장착. 좌클릭 단발, 우클릭 전탄 투척. 킬 시 단검 재충전.","duration":"킬 유지","type":"ultimate"},
     ]},
    {"id": "reyna",     "name": "레이나",  "role": "Duelist",    "origin": "멕시코",
     "desc": "멕시코 출신의 흡혈 결투사. 적을 처치할수록 강해지는 공격적인 플레이 스타일.",
     "abilities": [
         {"key":"C","name":"루메너리","desc":"적을 잠시 실명시키는 눈을 만든다. 적 사각지대에 배치 가능.","duration":"1.1초","type":"debuff"},
         {"key":"Q","name":"데보우","desc":"최근 처치한 적의 혼을 먹어 체력을 빠르게 회복한다.","duration":"1.5초 흡혈","type":"heal"},
         {"key":"E","name":"디스미스","desc":"혼을 소비해 무적 에너지 구체로 변신한다.","duration":"2초","type":"movement"},
         {"key":"X","name":"제국화","desc":"모든 능력이 강화되고 킬 시 자동으로 데보우/디스미스 발동.","duration":"30초","type":"ultimate"},
     ]},
    {"id": "neon",      "name": "네온",   "role": "Duelist",    "origin": "필리핀",
     "desc": "필리핀 출신 전기 결투사. 번개처럼 빠른 이동 속도와 전기 장벽으로 압도한다.",
     "abilities": [
         {"key":"C","name":"하이기어","desc":"전기 에너지를 뿜어 매우 빠른 속도로 달린다. 킬 시 초기화.","duration":"클리어","type":"movement"},
         {"key":"Q","name":"릴레이 볼트","desc":"전도성 볼트를 발사해 최대 두 번 튕기며 기절을 유발한다.","duration":"3초 기절","type":"debuff"},
         {"key":"E","name":"패스트레인","desc":"좁은 전기 장벽 두 개를 일직선으로 생성한다.","duration":"20초","type":"wall"},
         {"key":"X","name":"오버드라이브","desc":"번개 레이저를 조준사격. 전기 에너지 완충 시 활성화.","duration":"20초","type":"ultimate"},
     ]},
    {"id": "phoenix",   "name": "피닉스",  "role": "Duelist",    "origin": "영국",
     "desc": "영국 출신 불꽃 마법사. 자신에게는 불길이 치유이며 적에게는 파멸이다.",
     "abilities": [
         {"key":"C","name":"블레이즈","desc":"불꽃 벽을 생성한다. 시야를 차단하고 통과 시 피해.","duration":"8초","type":"wall"},
         {"key":"Q","name":"커브볼","desc":"커브를 그리는 플래시 수류탄으로 적을 실명시킨다.","duration":"1.1초","type":"flash"},
         {"key":"E","name":"핫 핸즈","desc":"불꽃 화염구를 던져 착지 후 폭발, 불꽃 지대 생성. 자신에겐 치유.","duration":"6초","type":"heal"},
         {"key":"X","name":"런잇백","desc":"마킹된 위치에서 부활한다.","duration":"10초","type":"ultimate"},
     ]},
    {"id": "raze",      "name": "레이즈",  "role": "Duelist",    "origin": "브라질",
     "desc": "브라질 출신 폭발물 전문가. 다양한 폭발물로 전장을 통제한다.",
     "abilities": [
         {"key":"C","name":"붐봇","desc":"폭발물이 장착된 로봇을 발사해 가장 가까운 적을 추적한다.","duration":"10초 또는 탐지","type":"trap"},
         {"key":"Q","name":"블라스트팩","desc":"폭발하는 배낭을 던진다. 자기 자신이나 적을 날릴 수 있다.","duration":"즉시","type":"movement"},
         {"key":"E","name":"페인트쉘","desc":"수류탄을 던지면 폭발 후 작은 수류탄 4개로 분열한다.","duration":"즉시","type":"damage"},
         {"key":"X","name":"쇼스토퍼","desc":"거대한 로켓런처 로켓을 발사해 폭발 피해를 입힌다.","duration":"즉시","type":"ultimate"},
     ]},
    {"id": "yoru",      "name": "요루",   "role": "Duelist",    "origin": "일본",
     "desc": "일본 출신 차원 이동자. 환상과 분신으로 적의 판단력을 흐린다.",
     "abilities": [
         {"key":"C","name":"페이크아웃","desc":"발자국 소리를 내는 분신을 생성, 격발 시 폭발해 실명.","duration":"즉시/1.5초","type":"decoy"},
         {"key":"Q","name":"블라인드사이드","desc":"불빛을 발사, 반사된 후 폭발해 실명.","duration":"1.75초","type":"flash"},
         {"key":"E","name":"게이트크래쉬","desc":"이동할 수 있는 포탈을 설치하고 즉시 텔레포트.","duration":"30초 포탈","type":"movement"},
         {"key":"X","name":"딤엔시어","desc":"차원에 들어가 완전한 은신 상태로 이동. 분신 소환 가능.","duration":"10초","type":"ultimate"},
     ]},
    {"id": "sova",      "name": "소바",   "role": "Initiator",  "origin": "러시아",
     "desc": "러시아 출신 정찰 전문가. 활과 드론으로 적의 위치를 정확히 파악한다.",
     "abilities": [
         {"key":"C","name":"아울 드론","desc":"드론을 조종해 적을 탐지하고 마크한다.","duration":"10초","type":"recon"},
         {"key":"Q","name":"충격 볼트","desc":"튕기는 충격 화살로 피해를 입힌다.","duration":"즉시","type":"damage"},
         {"key":"E","name":"정찰 볼트","desc":"정찰 화살을 발사, 착지 시 주변 적을 탐지한다.","duration":"12초","type":"recon"},
         {"key":"X","name":"헌터의 분노","desc":"에너지 광선을 발사해 벽을 통과한다. 최대 3번 발사.","duration":"즉시 (3회)","type":"ultimate"},
     ]},
    {"id": "skye",      "name": "스카이",  "role": "Initiator",  "origin": "호주",
     "desc": "호주 출신 자연의 수호자. 자연의 힘으로 팀을 지원하고 적을 제압한다.",
     "abilities": [
         {"key":"C","name":"트레일블레이저","desc":"호랑이 정령을 조종해 적을 기절시킨다.","duration":"5초/2.5초 기절","type":"stun"},
         {"key":"Q","name":"글린트","desc":"매 정령 플래시를 던진다. 조종해 방향 조정 가능.","duration":"2.25초","type":"flash"},
         {"key":"E","name":"가이딩 라이트","desc":"맹금류 정령을 조종해 이동. 적 탐지 시 실명.","duration":"6초 유지","type":"flash"},
         {"key":"X","name":"시커","desc":"세 마리 시커가 적을 추적하며 근접 시 근시 유발.","duration":"5초 추적","type":"debuff"},
     ]},
    {"id": "breach",    "name": "브리치",  "role": "Initiator",  "origin": "스웨덴",
     "desc": "스웨덴 출신 생체기계 팔의 소유자. 벽과 장애물을 통과하는 강력한 능력으로 공간을 장악한다.",
     "abilities": [
         {"key":"C","name":"어프레이스","desc":"벽 너머로 충격파를 발사해 적을 실명시킨다.","duration":"1.75초","type":"flash"},
         {"key":"Q","name":"폴트라인","desc":"강력한 지진파로 벽을 통과해 콘크리트 흔들기.","duration":"2.5초 혼란","type":"debuff"},
         {"key":"E","name":"애프터쇼크","desc":"벽을 통과해 대형 폭발을 발생시킨다.","duration":"즉시","type":"damage"},
         {"key":"X","name":"롤링 선더","desc":"거대한 지진파로 적을 공중으로 띄운다.","duration":"6초","type":"ultimate"},
     ]},
    {"id": "kayo",      "name": "KAY/O",  "role": "Initiator",  "origin": "미래",
     "desc": "미래에서 온 전투 기계. 요원의 능력을 억제하는 기술로 전장을 통제한다.",
     "abilities": [
         {"key":"C","name":"FLASH/drive","desc":"투척 후 폭발하는 플래시 장치. 누름 시간에 따라 타이밍 조절.","duration":"0.75초","type":"flash"},
         {"key":"Q","name":"ZERO/point","desc":"능력을 억제하는 블레이드를 던진다.","duration":"8초 억제","type":"suppress"},
         {"key":"E","name":"FRAG/ment","desc":"착지 후 다수 폭발하는 폭발물 조각.","duration":"3초/4회","type":"damage"},
         {"key":"X","name":"NULL/cmd","desc":"에너지 과부하로 넓은 범위 능력 억제.","duration":"10초","type":"ultimate"},
     ]},
    {"id": "fade",      "name": "페이드",  "role": "Initiator",  "origin": "튀르키예",
     "desc": "튀르키예 출신 악몽의 수집가. 적의 두려움을 수집해 무기로 사용한다.",
     "abilities": [
         {"key":"C","name":"시즈","desc":"적을 포획하고 노이즈를 유발하는 악몽을 소환한다.","duration":"6초","type":"trap"},
         {"key":"Q","name":"하운트","desc":"정찰 악몽을 생성, 추적 시 위치 노출.","duration":"12초","type":"recon"},
         {"key":"E","name":"프로울러","desc":"적을 감지하면 추격하여 근시 유발.","duration":"2.5초 근시","type":"debuff"},
         {"key":"X","name":"나이트폴","desc":"거대한 악몽 지대를 생성해 근시, 청각장애, 디케이를 유발.","duration":"12초","type":"ultimate"},
     ]},
    {"id": "omen",      "name": "오멘",   "role": "Controller", "origin": "알 수 없음",
     "desc": "알 수 없는 존재에서 귀환한 그림자. 어둠과 순간이동을 자유자재로 다룬다.",
     "abilities": [
         {"key":"C","name":"서로잉다크니스","desc":"수축하는 연기 구체로 시야를 차단한다.","duration":"15초","type":"smoke"},
         {"key":"Q","name":"패런이어","desc":"짧은 거리의 플래시 구체를 던진다.","duration":"1.5초","type":"flash"},
         {"key":"E","name":"다크커버","desc":"구체를 발사해 연기 스크린을 설치한다.","duration":"15초","type":"smoke"},
         {"key":"X","name":"프롬더섀도우즈","desc":"맵 어디든 순간이동한다. 취소 가능.","duration":"즉시","type":"ultimate"},
     ]},
    {"id": "astra",     "name": "아스트라", "role": "Controller", "origin": "가나",
     "desc": "가나 출신 우주 마법사. 별의 힘을 이용해 전장 전체를 원격으로 제어한다.",
     "abilities": [
         {"key":"C","name":"노바 펄스","desc":"별을 소환 후 기폭해 기절을 유발한다.","duration":"1.7초 기절","type":"stun"},
         {"key":"Q","name":"네뷸라","desc":"별을 연기로 변환한다.","duration":"15초","type":"smoke"},
         {"key":"E","name":"그래비티 웰","desc":"별 위치에 블랙홀을 생성해 당긴다.","duration":"3초","type":"trap"},
         {"key":"X","name":"아스트랄 폼","desc":"아스트랄 차원에 들어가 전체 맵에 별을 설치한다.","duration":"무제한(별 유지)","type":"ultimate"},
     ]},
    {"id": "brimstone", "name": "브림스톤", "role": "Controller", "origin": "미국",
     "desc": "미국 출신 베테랑 전술가. 하늘에서 지원 폭격과 스모크를 통해 전장을 지배한다.",
     "abilities": [
         {"key":"C","name":"인센다리","desc":"소이탄을 투척해 화염 지대를 생성한다.","duration":"8초","type":"damage"},
         {"key":"Q","name":"스카이스모크","desc":"태블릿으로 맵 어디서든 연기 투하.","duration":"19초","type":"smoke"},
         {"key":"E","name":"스팀 비컨","desc":"속도 증가 비컨을 설치한다.","duration":"15초","type":"buff"},
         {"key":"X","name":"오비탈 스트라이크","desc":"강력한 레이저 폭격을 지정 위치에 투하.","duration":"4초","type":"ultimate"},
     ]},
    {"id": "viper",     "name": "바이퍼",  "role": "Controller", "origin": "미국",
     "desc": "미국 출신 독극물 전문가. 유독 가스와 연기로 전장 전체를 오염시킨다.",
     "abilities": [
         {"key":"C","name":"스네이크바이트","desc":"독성 웅덩이를 생성하는 발사체를 발사한다.","duration":"6.5초","type":"damage"},
         {"key":"Q","name":"포이즌 클라우드","desc":"독성 연기 방출 장치를 설치한다.","duration":"연료 소모시","type":"smoke"},
         {"key":"E","name":"토식 스크린","desc":"긴 독성 연기 벽을 생성한다.","duration":"연료 소모시","type":"wall"},
         {"key":"X","name":"바이퍼스 핏","desc":"전체 공간을 독성 연기로 채운다.","duration":"15초+킬 유지","type":"ultimate"},
     ]},
    {"id": "harbor",    "name": "하버",   "role": "Controller", "origin": "인도",
     "desc": "인도 출신 물의 수호자. 고대 유물의 힘으로 물을 자유롭게 다룬다.",
     "abilities": [
         {"key":"C","name":"캐스케이드","desc":"파도 벽을 생성해 통과하는 적을 느리게 한다.","duration":"6초","type":"wall"},
         {"key":"Q","name":"쿠버","desc":"고리 모양 물 연기를 생성한다.","duration":"6.25초","type":"smoke"},
         {"key":"E","name":"하이타이드","desc":"물 벽을 원하는 방향으로 조종한다.","duration":"12초","type":"wall"},
         {"key":"X","name":"래쉬","desc":"물 소용돌이 세 개를 생성해 교대로 지면을 두드린다.","duration":"5초/3회","type":"ultimate"},
     ]},
    {"id": "sage",      "name": "세이지",  "role": "Sentinel",   "origin": "중국",
     "desc": "중국 출신 치유사. 팀의 생명을 유지하고 전략적 장벽으로 공간을 통제한다.",
     "abilities": [
         {"key":"C","name":"슬로우 오브","desc":"느리게 하는 구체를 던진다.","duration":"5.5초","type":"debuff"},
         {"key":"Q","name":"배리어 오브","desc":"거대한 얼음 벽을 생성한다.","duration":"40초","type":"wall"},
         {"key":"E","name":"힐링 오브","desc":"자신 또는 아군을 치유한다.","duration":"5초 힐링","type":"heal"},
         {"key":"X","name":"부활","desc":"아군 요원 하나를 원래 체력으로 부활시킨다.","duration":"즉시","type":"ultimate"},
     ]},
    {"id": "cypher",    "name": "사이퍼",  "role": "Sentinel",   "origin": "모로코",
     "desc": "모로코 출신 정보 수집가. 다양한 함정과 감시 장치로 모든 것을 감시한다.",
     "abilities": [
         {"key":"C","name":"사이버케이지","desc":"이동식 원격 함정을 설치해 비활성화 가능.","duration":"7초","type":"trap"},
         {"key":"Q","name":"스파이캠","desc":"원격 카메라를 설치해 적 탐지 및 독침 발사.","duration":"영구","type":"recon"},
         {"key":"E","name":"트랩와이어","desc":"두 벽 사이에 철사 함정을 설치한다.","duration":"영구","type":"trap"},
         {"key":"X","name":"뉴럴 도용","desc":"처치된 적에게서 적 위치 정보를 추출한다.","duration":"즉시","type":"ultimate"},
     ]},
    {"id": "killjoy",   "name": "킬조이",  "role": "Sentinel",   "origin": "독일",
     "desc": "독일 출신 천재 발명가. 자신이 제작한 기계 장치들로 구역을 완벽하게 방어한다.",
     "abilities": [
         {"key":"C","name":"어람봇","desc":"적 탐지 시 폭발하는 로봇을 설치한다.","duration":"영구(사망 전)","type":"trap"},
         {"key":"Q","name":"나노스웜","desc":"폭발 후 분열하는 수류탄.","duration":"12초 지대","type":"damage"},
         {"key":"E","name":"터렛","desc":"자동 사격 포탑을 설치한다.","duration":"영구(사망 전)","type":"trap"},
         {"key":"X","name":"록다운","desc":"범위 내 적을 기절시키는 장치를 설치한다.","duration":"기절 영구(장치 유지)","type":"ultimate"},
     ]},
    {"id": "deadlock",  "name": "데드락",  "role": "Sentinel",   "origin": "노르웨이",
     "desc": "노르웨이 출신 감시 전문가. 나노와이어 기술로 적의 이동과 부활을 차단한다.",
     "abilities": [
         {"key":"C","name":"그레이브바인드","desc":"GravNet 수류탄을 던져 적을 포박해 웅크리게 한다.","duration":"3초","type":"trap"},
         {"key":"Q","name":"소닉 센서","desc":"진동을 감지해 폭발하는 센서를 설치한다.","duration":"영구","type":"trap"},
         {"key":"E","name":"배리어 메시","desc":"통과를 차단하는 나노와이어 배리어를 생성한다.","duration":"30초","type":"wall"},
         {"key":"X","name":"아나이얼레이션","desc":"적을 나노와이어 코쿤에 포획해 처치한다.","duration":"처치 시까지","type":"ultimate"},
     ]},
]

# ── 세션 상태 ─────────────────────────────────────────────────────────────────
if "selected" not in st.session_state:
    st.session_state.selected = None
if "role_filter" not in st.session_state:
    st.session_state.role_filter = "all"

# ── 헤더 ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="val-header">
  <div>
    <div class="val-logo">VALO<span>RANT</span></div>
    <div class="val-subtitle">// AGENT COMPENDIUM — TACTICAL DATABASE v2.0</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── 필터 버튼 ─────────────────────────────────────────────────────────────────
role_filter = st.session_state.role_filter
filtered = AGENTS if role_filter == "all" else [a for a in AGENTS if a["role"] == role_filter]

btn_cols = st.columns([1.2, 1, 1, 1, 1])
labels = [f"전체 ({len(AGENTS)})", f"⚔️ 결투사 ({sum(1 for a in AGENTS if a['role']=='Duelist')})",
          f"🔍 개시자 ({sum(1 for a in AGENTS if a['role']=='Initiator')})",
          f"💨 조종사 ({sum(1 for a in AGENTS if a['role']=='Controller')})",
          f"🛡️ 감시자 ({sum(1 for a in AGENTS if a['role']=='Sentinel')})"]
keys  = ["all", "Duelist", "Initiator", "Controller", "Sentinel"]

for col, lbl, key in zip(btn_cols, labels, keys):
    with col:
        if st.button(lbl, key=f"filter_{key}", use_container_width=True,
                     type="primary" if role_filter == key else "secondary"):
            st.session_state.role_filter = key
            st.session_state.selected = None
            st.rerun()

st.caption(f"AGENTS: {len(filtered)}")

# ── 상세 패널 ─────────────────────────────────────────────────────────────────
if st.session_state.selected:
    agent = next((a for a in AGENTS if a["id"] == st.session_state.selected), None)
    if agent:
        r = ROLES[agent["role"]]
        abilities_html = ""
        for ab in agent["abilities"]:
            tc = TYPE_COLORS.get(ab["type"], "#888")
            abilities_html += f"""
            <div class="ability-row">
              <div class="ability-key">
                <div class="key-label">{ab['key']}</div>
                <div class="key-sub">능력키</div>
              </div>
              <div>
                <div class="ability-name">{ab['name']}</div>
                <div class="ability-desc">{ab['desc']}</div>
                <span class="ability-tag" style="background:{tc}22;color:{tc};border:1px solid {tc}44">{ab['type']}</span>
              </div>
              <div class="ability-duration" style="text-align:right;min-width:80px">
                <div class="dur-val">{ab['duration']}</div>
                <div class="dur-label">지속 시간</div>
              </div>
            </div>"""

        st.markdown(f"""
        <div class="detail-panel">
          <div class="detail-header" style="display:flex;justify-content:space-between;margin-bottom:18px">
            <div>
              <div class="detail-name">{agent['name']}</div>
              <div class="detail-role">{r['icon']} {r['label']} &nbsp;// {agent['origin']}</div>
            </div>
            <div style="font-family:'Share Tech Mono',monospace;font-size:12px;color:#7a8c99;text-align:right;line-height:1.9">
              능력 {len(agent['abilities'])}개<br>ID: {agent['id'].upper()}
            </div>
          </div>
          <div class="detail-desc">{agent['desc']}</div>
          <div class="abilities-title">// 능력 목록 및 지속 시간</div>
          {abilities_html}
        </div>
        """, unsafe_allow_html=True)

        if st.button("✕ 닫기", key="close_detail"):
            st.session_state.selected = None
            st.rerun()

# ── 카드 그리드 ───────────────────────────────────────────────────────────────
cols = st.columns(4)
for i, agent in enumerate(filtered):
    r = ROLES[agent["role"]]
    is_selected = st.session_state.selected == agent["id"]
    with cols[i % 4]:
        selected_class = "agent-card-selected" if is_selected else ""
        st.markdown(f"""
        <div class="agent-card {selected_class}">
          <div style="display:flex;align-items:center;gap:10px">
            <div style="width:38px;height:38px;border-radius:2px;display:flex;align-items:center;
                        justify-content:center;font-size:18px;
                        background:{r['color']}22;border:1px solid {r['color']}44">
              {r['icon']}
            </div>
            <div>
              <div class="card-name">{agent['name']}</div>
              <div class="card-role">{r['label']}</div>
            </div>
          </div>
          <div class="card-origin">📍 {agent['origin']}</div>
          <div style="height:2px;background:{r['color']}55;margin-top:8px"></div>
        </div>
        """, unsafe_allow_html=True)

        btn_label = "▶ 선택됨" if is_selected else "상세 보기"
        if st.button(btn_label, key=f"agent_{agent['id']}", use_container_width=True,
                     type="primary" if is_selected else "secondary"):
            if is_selected:
                st.session_state.selected = None
            else:
                st.session_state.selected = agent["id"]
            st.rerun()

# ── 푸터 ─────────────────────────────────────────────────────────────────────
st.divider()
st.caption("// VALORANT AGENT COMPENDIUM — 능력 지속 시간은 패치에 따라 변동될 수 있습니다")
