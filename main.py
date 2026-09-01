import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────
# 페이지 기본 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🎬 영화 데이터 그래프 도감",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# 커스텀 CSS 스타일
# ─────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #0f0f1a;
        color: #ffffff;
    }
    .main-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e50914, #ff6b6b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0 5px 0;
        letter-spacing: 2px;
    }
    .sub-title {
        text-align: center;
        color: #aaaaaa;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffd700;
        border-left: 4px solid #e50914;
        padding-left: 12px;
        margin: 10px 0 20px 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #333355;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.15);
    }
    .metric-label {
        color: #aaaaaa;
        font-size: 0.85rem;
        margin-bottom: 6px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .metric-value {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
    }
    .metric-value-highlight {
        color: #ffd700;
        font-size: 1.6rem;
        font-weight: 800;
    }
    .info-box {
        background: linear-gradient(135deg, #1a2a1a, #0f1f0f);
        border: 1px solid #2a5a2a;
        border-radius: 10px;
        padding: 15px 20px;
        color: #90ee90;
        font-size: 0.95rem;
        margin-top: 15px;
    }
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e50914, transparent);
        margin: 30px 0;
    }
    [data-testid="stSidebar"] {
        background-color: #12121f;
        border-right: 1px solid #333355;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 데이터 불러오기 (캐싱 적용)
# ─────────────────────────────────────────
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url, encoding='utf-8')
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

df = load_data()


# ─────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎬 영화 선택")
    st.markdown("---")

    movie_list     = sorted(df['영화명'].unique())
    selected_movie = st.selectbox(
        "영화를 선택하세요",
        movie_list,
        help="1번 그래프에서 분석할 영화를 선택합니다."
    )

    st.markdown("---")
    st.markdown("### 📋 데이터 정보")
    st.markdown(f"- **총 영화 수:** {df['영화명'].nunique()}편")
    st.markdown(f"- **데이터 기간:** {df['날짜'].min().strftime('%Y.%m.%d')} ~ {df['날짜'].max().strftime('%Y.%m.%d')}")
    st.markdown(f"- **총 레코드 수:** {len(df):,}건")
    st.markdown("---")
    st.caption("📌 출처: 영화진흥위원회 (KOBIS)")


# ─────────────────────────────────────────
# 메인 타이틀
# ─────────────────────────────────────────
st.markdown('<div class="main-title">🎬 영화 데이터 그래프 도감</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">영화진흥위원회 일별 박스오피스 데이터 분석 대시보드</div>', unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 섹션 1: 영화별 일관객 변화 추이
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📈 1. 영화별 일관객 변화 추이</div>', unsafe_allow_html=True)

filtered_df = df[df['영화명'] == selected_movie].copy()
filtered_df = filtered_df.sort_values('날짜')

# ── 핵심 지표 카드 ──────────────────────
total_audience = int(filtered_df['일관객'].sum())
max_audience   = int(filtered_df['일관객'].max())
avg_audience   = int(filtered_df['일관객'].mean())
peak_date      = filtered_df.loc[filtered_df['일관객'].idxmax(), '날짜'].strftime('%m월 %d일')

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🎟️ 누적 관객수</div>
        <div class="metric-value-highlight">{total_audience:,}명</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🏆 최고 일 관객수</div>
        <div class="metric-value">{max_audience:,}명</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📊 평균 일 관객수</div>
        <div class="metric-value">{avg_audience:,}명</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">📅 최고 흥행일</div>
        <div class="metric-value">{peak_date}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 선 그래프 ───────────────────────────
fig1 = px.line(
    filtered_df,
    x='날짜',
    y='일관객',
    title=f"<b>'{selected_movie}'</b> 일별 관객수 추이",
    markers=True,
    labels={'날짜': '상영 날짜', '일관객': '일일 관객수 (명)'},
    color_discrete_sequence=['#e50914']
)

peak_row = filtered_df.loc[filtered_df['일관객'].idxmax()]
fig1.add_scatter(
    x=[peak_row['날짜']],
    y=[peak_row['일관객']],
    mode='markers',
    marker=dict(size=14, color='#ffd700', symbol='star'),
    name='최고 흥행일',
    hovertemplate=f"<b>최고 흥행일</b><br>날짜: {peak_row['날짜'].strftime('%Y-%m-%d')}<br>관객수: {int(peak_row['일관객']):,}명<extra></extra>"
)

fig1.update_traces(
    hovertemplate='<b>날짜</b>: %{x|%Y-%m-%d}<br><b>관객수</b>: %{y:,}명<extra></extra>',
    selector=dict(mode='lines+markers')
)

fig1.update_layout(
    plot_bgcolor='#12121f',
    paper_bgcolor='#12121f',
    font=dict(color='#cccccc', family='Malgun Gothic, sans-serif'),
    title=dict(font=dict(size=18, color='#ffffff'), x=0.5, xanchor='center'),
    xaxis=dict(showgrid=True, gridcolor='#222244', tickformat='%Y-%m-%d',
               tickangle=-30, title_font=dict(color='#aaaaaa')),
    yaxis=dict(showgrid=True, gridcolor='#222244', tickformat=',',
               title_font=dict(color='#aaaaaa')),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#333355', borderwidth=1),
    hovermode='x unified',
    margin=dict(t=60, b=40, l=60, r=30),
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown(f"""
<div class="info-box">
💡 <b>이 그래프로 알 수 있는 것:</b>
개봉 초반 관객이 집중되고 이후 감소하는 흥행 패턴을 확인할 수 있습니다.
<b>'{selected_movie}'</b>의 누적 관객은 <b>{total_audience:,}명</b>이며,
가장 많은 관객이 몰린 날은 <b>{peak_date} ({max_audience:,}명)</b>입니다.
</div>
""", unsafe_allow_html=True)

with st.expander("📋 상세 데이터 보기"):
    display_df = filtered_df[['날짜', '일관객']].copy()
    display_df['날짜']  = display_df['날짜'].dt.strftime('%Y-%m-%d')
    display_df['일관객'] = display_df['일관객'].apply(lambda x: f"{int(x):,}명")
    display_df = display_df.rename(columns={'날짜': '상영 날짜', '일관객': '일일 관객수'})
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ─────────────────────────────────────────
# 섹션 2: TOP 5 영화 일관객 비교
# ─────────────────────────────────────────
st.markdown('<div class="section-header">🏆 2. 흥행 TOP 5 영화 일관객 비교</div>', unsafe_allow_html=True)

# ── TOP 5 영화 추출 ──────────────────────
top5_movies = (
    df.groupby('영화명')['일관객']
    .sum()
    .nlargest(5)
    .reset_index()
)
top5_names = top5_movies['영화명'].tolist()
top5_df    = df[df['영화명'].isin(top5_names)].copy()
top5_df    = top5_df.sort_values('날짜')

# ── TOP 5 순위 카드 ──────────────────────
st.markdown("#### 📊 기간 내 누적 관객 순위")

COLORS = ['#e50914', '#ffd700', '#00cfff', '#ff7f50', '#90ee90']

cols = st.columns(5)
for i, row in top5_movies.iterrows():
    rank  = i + 1
    color = COLORS[i]
    with cols[i]:
        st.markdown(f"""
        <div class="metric-card"
             style="border-color:{color};
                    box-shadow: 0 4px 15px {color}44;">
            <div class="metric-label" style="color:{color};">
                {'🥇' if rank==1 else '🥈' if rank==2 else '🥉' if rank==3 else f'{rank}위'}
            </div>
            <div style="font-size:0.9rem; font-weight:700;
                        color:#ffffff; margin:6px 0 4px 0;
                        white-space:nowrap; overflow:hidden;
                        text-overflow:ellipsis;"
                 title="{row['영화명']}">
                {row['영화명']}
            </div>
            <div style="color:{color}; font-size:1.1rem; font-weight:800;">
                {int(row['일관객']):,}명
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── 멀티 선 그래프 ───────────────────────
fig2 = px.line(
    top5_df,
    x='날짜',
    y='일관객',
    color='영화명',
    title='<b>흥행 TOP 5</b> 영화 일별 관객수 비교',
    markers=False,
    labels={'날짜': '상영 날짜', '일관객': '일일 관객수 (명)', '영화명': '영화'},
    color_discrete_sequence=COLORS,
)

fig2.update_traces(
    hovertemplate='<b>%{fullData.name}</b><br>날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>',
    line=dict(width=2.5),
)

fig2.update_layout(
    plot_bgcolor='#12121f',
    paper_bgcolor='#12121f',
    font=dict(color='#cccccc', family='Malgun Gothic, sans-serif'),
    title=dict(font=dict(size=18, color='#ffffff'), x=0.5, xanchor='center'),
    xaxis=dict(
        showgrid=True, gridcolor='#222244',
        tickformat='%Y-%m-%d', tickangle=-30,
        title_font=dict(color='#aaaaaa'),
    ),
    yaxis=dict(
        showgrid=True, gridcolor='#222244',
        tickformat=',',
        title_font=dict(color='#aaaaaa'),
    ),
    legend=dict(
        title='🎬 영화 (클릭으로 켜기/끄기)',
        bgcolor='rgba(18,18,31,0.9)',
        bordercolor='#333355',
        borderwidth=1,
        font=dict(size=12),
        itemclick='toggle',          # 클릭 → 토글
        itemdoubleclick='toggleothers',  # 더블클릭 → 단독 표시
    ),
    hovermode='x unified',
    margin=dict(t=60, b=40, l=60, r=30),
)

st.plotly_chart(fig2, use_container_width=True)

# ── 사용 안내 ────────────────────────────
st.markdown("""
<div class="info-box">
💡 <b>그래프 사용법:</b>
오른쪽 범례에서 영화 이름을 <b>한 번 클릭</b>하면 해당 영화를 숨기거나 다시 표시할 수 있습니다.
<b>더블클릭</b>하면 해당 영화만 단독으로 볼 수 있어요.
흥행 1위 영화와 나머지 영화의 관객 곡선 모양을 비교해 보세요!
</div>
""", unsafe_allow_html=True)

# ── 상세 데이터 테이블 (토글) ───────────
with st.expander("📋 TOP 5 영화 누적 관객 상세 보기"):
    display_top5 = top5_movies.copy()
    display_top5.index = ['🥇 1위', '🥈 2위', '🥉 3위', '4위', '5위']
    display_top5.columns = ['영화명', '누적 관객수']
    display_top5['누적 관객수'] = display_top5['누적 관객수'].apply(lambda x: f"{int(x):,}명")
    st.dataframe(display_top5, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)
