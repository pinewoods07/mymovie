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
    df['openDt'] = pd.to_datetime(df['openDt'].astype(str), format='%Y%m%d')
    df['genre']  = df['genre'].astype(str).str.split('|').str[0].str.strip()
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
st.markdown("<hr>", unsafe_allow_html=True)


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
    hole=0.45,
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
    title=dict(text='<b>장르별 영화 편수</b>',
               font=dict(size=17, color='#ffffff'), x=0.5, xanchor='center'),
    legend=dict(bgcolor='rgba(18,18,31,0.9)', bordercolor='#333355',
                borderwidth=1, font=dict(size=11)),
    margin=dict(t=60, b=40, l=40, r=40),
)
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

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 2: 장르 × 영화 트리맵 (총 관객 기준)
# ═════════════════════════════════════════
st.markdown('<div class="section-header">🗺️ 2. 장르별 · 영화별 총 관객 트리맵</div>',
            unsafe_allow_html=True)

# total_audi 가 0 이하인 행 제거 (트리맵은 양수만 허용)
tree_df = df[df['total_audi'] > 0].copy()

fig2 = px.treemap(
    tree_df,
    path=['genre', 'movieNm'],        # 장르 → 영화명 계층
    values='total_audi',
    color='genre',
    color_discrete_sequence=DONUT_COLORS,
    custom_data=['movieNm', 'total_audi'],
)

# 호버 툴팁 커스터마이징
fig2.update_traces(
    hovertemplate=(
        '<b>%{customdata[0]}</b><br>'
        '총 관객: %{customdata[1]:,}명'
        '<extra></extra>'
    ),
    textfont=dict(size=13),
    # 칸 안에 영화명 표시
    texttemplate='%{label}',
    marker=dict(line=dict(width=1, color='#0f0f1a')),
)

fig2.update_layout(
    **BASE_LAYOUT,
    title=dict(text='<b>장르별 영화 총 관객 트리맵</b> (칸 크기 = 총 관객수)',
               font=dict(size=17, color='#ffffff'), x=0.5, xanchor='center'),
    margin=dict(t=60, b=20, l=10, r=10),
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class="info-box">
💡 <b>이 그래프로 알 수 있는 것:</b>
칸이 클수록 총 관객이 많은 영화입니다. 같은 장르 안에서도 영화별 흥행 격차가 크며,
어떤 장르가 전체 관객을 많이 끌어모았는지 한눈에 비교할 수 있습니다.
</div>
""", unsafe_allow_html=True)

with st.expander("📋 트리맵 원본 데이터 (총 관객 상위 20편)"):
    show2 = (tree_df[['movieNm','genre','total_audi']]
             .sort_values('total_audi', ascending=False)
             .head(20)
             .copy())
    show2.index = range(1, len(show2)+1)
    show2['total_audi'] = show2['total_audi'].apply(lambda x: f"{int(x):,}명")
    show2.columns = ['영화명','장르','총 관객수']
    st.dataframe(show2, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 3: 총 관객 히스토그램
# ═════════════════════════════════════════
st.markdown('<div class="section-header">📊 3. 총 관객 분포 히스토그램</div>',
            unsafe_allow_html=True)

# 분포 파악용 수치 계산
max_row    = df.loc[df['total_audi'].idxmax()]
max_movie  = max_row['movieNm']
max_audi   = int(max_row['total_audi'])
median_val = int(df['total_audi'].median())
q75_val    = int(df['total_audi'].quantile(0.75))

fig3 = go.Figure()

fig3.add_trace(go.Histogram(
    x=df['total_audi'],
    nbinsx=30,
    marker=dict(
        color='#e50914',
        line=dict(color='#0f0f1a', width=1),
        opacity=0.85,
    ),
    hovertemplate='관객 구간: %{x:,}명<br>영화 수: %{y}편<extra></extra>',
    name='영화 수',
))

# 중앙값 수직선
fig3.add_vline(
    x=median_val,
    line=dict(color='#ffd700', width=2, dash='dash'),
    annotation=dict(
        text=f"중앙값<br>{median_val:,}명",
        font=dict(color='#ffd700', size=11),
        bgcolor='rgba(15,15,26,0.8)',
        bordercolor='#ffd700',
    ),
    annotation_position='top right',
)

# 최대값 수직선
fig3.add_vline(
    x=max_audi,
    line=dict(color='#00cfff', width=2, dash='dot'),
    annotation=dict(
        text=f"최고 흥행<br>{max_movie}<br>{max_audi:,}명",
        font=dict(color='#00cfff', size=11),
        bgcolor='rgba(15,15,26,0.8)',
        bordercolor='#00cfff',
    ),
    annotation_position='top left',
)

fig3.update_layout(
    **BASE_LAYOUT,
    title=dict(text='<b>총 관객 분포</b>',
               font=dict(size=17, color='#ffffff'), x=0.5, xanchor='center'),
    xaxis=dict(
        title='총 관객수 (명)', title_font=dict(color='#aaaaaa'),
        showgrid=True, gridcolor='#222244', tickformat=',',
    ),
    yaxis=dict(
        title='영화 편수', title_font=dict(color='#aaaaaa'),
        showgrid=True, gridcolor='#222244',
    ),
    bargap=0.05,
    hovermode='x unified',
    margin=dict(t=60, b=40, l=60, r=30),
)

st.plotly_chart(fig3, use_container_width=True)

# ── 동적 분석 문구 ───────────────────────
under_100 = int((df['total_audi'] < 1_000_000).sum())
pct_under = round(under_100 / len(df) * 100, 1)

st.markdown(f"""
<div class="info-box">
💡 <b>이 그래프로 알 수 있는 것:</b>
전체 {len(df)}편 중 <b>{under_100}편({pct_under}%)</b>이 총 관객 100만 명 미만에 분포하며,
대부분의 영화가 소수 관객에 그치는 반면,
가장 관객이 많은 영화는 <b>'{max_movie}'({max_audi:,}명)</b>으로
중앙값({median_val:,}명)의 <b>{round(max_audi/median_val, 1)}배</b>에 달합니다.
</div>
""", unsafe_allow_html=True)

with st.expander("📋 총 관객 기초 통계"):
    stat = df['total_audi'].describe().rename({
        'count':'편수','mean':'평균','std':'표준편차',
        'min':'최솟값','25%':'하위 25%','50%':'중앙값',
        '75%':'상위 25%','max':'최댓값'
    })
    stat_df = pd.DataFrame({'값': stat.apply(lambda x: f"{int(x):,}명")})
    st.dataframe(stat_df, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 이후 그래프 자리 (확장용)
# ═════════════════════════════════════════
st.markdown('<div class="section-header">📈 4. (다음 그래프 제목을 입력하세요)</div>',
            unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
📌 이곳에 다음 그래프와 코드를 추가할 수 있습니다.
</div>
""", unsafe_allow_html=True)
