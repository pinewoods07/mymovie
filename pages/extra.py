import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🎬 영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0f0f1a; color: #ffffff; }
    .section-header {
        font-size: 1.3rem; font-weight: 700; color: #ffd700;
        border-left: 4px solid #e50914;
        padding-left: 12px; margin: 10px 0 20px 0;
    }
    .info-box {
        background: #1a2a1a; border: 1px solid #2a5a2a;
        border-radius: 10px; padding: 14px 18px;
        color: #90ee90; font-size: 0.92rem; margin-top: 12px;
    }
    hr {
        border: none; height: 1px;
        background: linear-gradient(90deg, transparent, #e50914, transparent);
        margin: 28px 0;
    }
    [data-testid="stSidebar"] {
        background-color: #12121f;
        border-right: 1px solid #333355;
    }
</style>
""", unsafe_allow_html=True)

BASE_LAYOUT = dict(
    plot_bgcolor='#12121f',
    paper_bgcolor='#12121f',
    font=dict(color='#cccccc', family='Malgun Gothic, sans-serif'),
)

# ─────────────────────────────────────────
# 데이터 로드
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
    df = pd.read_csv(url, encoding='utf-8')

    # 개봉일 변환
    df['openDt'] = pd.to_datetime(df['openDt'].astype(str), format='%Y%m%d')

    # 장르: 세로막대(|)로 구분된 경우 첫 번째만 사용
    df['genre'] = df['genre'].astype(str).str.split('|').str[0].str.strip()

    return df

df = load_data()

# ─────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎬 데이터 정보")
    st.markdown("---")
    st.markdown(f"**총 영화 수:** {len(df)}편")
    st.markdown(f"**장르 수:** {df['genre'].nunique()}개")
    st.markdown(f"**제작 국가 수:** {df['nation'].nunique()}개")
    st.markdown(f"**개봉 기간:** {df['openDt'].min().strftime('%Y.%m.%d')} ~ {df['openDt'].max().strftime('%Y.%m.%d')}")
    st.markdown("---")
    st.caption("출처: 영화진흥위원회 (KOBIS)")

# ─────────────────────────────────────────
# 타이틀
# ─────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; font-size:2.4rem; font-weight:800;
           background:linear-gradient(90deg,#e50914,#ff6b6b,#ffd700);
           -webkit-background-clip:text; -webkit-text-fill-color:transparent;
           padding: 16px 0 4px 0;'>
    🎬 영화 데이터 그래프 도감 2
</h1>
<p style='text-align:center; color:#aaaaaa; margin-bottom:24px;'>
    분포와 관계 — 216편 요약 데이터 분석
</p>
""", unsafe_allow_html=True)
st.markdown("<hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,#e50914,transparent);margin:28px 0;'>",
            unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 1: 장르별 영화 편수 도넛 그래프
# ═════════════════════════════════════════
st.markdown('<div class="section-header">🍩 1. 장르별 영화 편수</div>',
            unsafe_allow_html=True)

genre_count = (df.groupby('genre')
                 .size()
                 .reset_index(name='편수')
                 .sort_values('편수', ascending=False))

DONUT_COLORS = [
    '#e50914','#ffd700','#00cfff','#ff7f50','#90ee90',
    '#da70d6','#87ceeb','#f08080','#98fb98','#dda0dd',
    '#b0c4de','#ffe4b5','#afeeee','#ffb6c1','#d3d3d3',
]

fig1 = go.Figure(data=go.Pie(
    labels=genre_count['genre'],
    values=genre_count['편수'],
    hole=0.45,                          # 도넛 구멍 크기
    marker=dict(
        colors=DONUT_COLORS[:len(genre_count)],
        line=dict(color='#0f0f1a', width=2)
    ),
    hovertemplate=(
        '<b>%{label}</b><br>'
        '편수: %{value}편<br>'
        '비율: %{percent}<br>'
        '<extra></extra>'
    ),
    textinfo='label+percent',
    textfont=dict(size=12, color='#ffffff'),
    insidetextorientation='auto',
))

fig1.update_layout(
    **BASE_LAYOUT,
    title=dict(
        text='<b>장르별 영화 편수</b>',
        font=dict(size=17, color='#ffffff'),
        x=0.5, xanchor='center'
    ),
    legend=dict(
        bgcolor='rgba(18,18,31,0.9)',
        bordercolor='#333355', borderwidth=1,
        font=dict(size=11),
        orientation='v',
    ),
    margin=dict(t=60, b=40, l=40, r=40),
)

# 가운데 텍스트 annotation
fig1.add_annotation(
    text=f"총<br><b>{len(df)}편</b>",
    x=0.5, y=0.5,
    font=dict(size=16, color='#ffffff'),
    showarrow=False
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
<div class="info-box">
💡 <b>이 그래프로 알 수 있는 것:</b>
박스오피스 10위권에 오른 영화는 드라마·액션 장르가 압도적으로 많으며,
특정 장르가 흥행을 주도하는 경향을 확인할 수 있습니다.
</div>
""", unsafe_allow_html=True)

with st.expander("📋 장르별 편수 상세"):
    show1 = genre_count.copy()
    show1['비율'] = (show1['편수'] / show1['편수'].sum() * 100).round(1).astype(str) + '%'
    show1.index = range(1, len(show1)+1)
    st.dataframe(show1.rename(columns={'genre':'장르'}), use_container_width=True)

st.markdown("<hr style='border:none;height:1px;background:linear-gradient(90deg,transparent,#e50914,transparent);margin:28px 0;'>",
            unsafe_allow_html=True)

# ═════════════════════════════════════════
# 이후 그래프 자리 (확장용)
# ═════════════════════════════════════════
st.markdown('<div class="section-header">📊 2. (다음 그래프 제목을 입력하세요)</div>',
            unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
📌 이곳에 다음 그래프와 코드를 추가할 수 있습니다.
</div>
""", unsafe_allow_html=True)
