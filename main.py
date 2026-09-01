import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🎬 영화 데이터 그래프 도감",
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

# ─────────────────────────────────────────
# 공통 그래프 레이아웃
# ─────────────────────────────────────────
CHART_LAYOUT = dict(
    plot_bgcolor='#12121f',
    paper_bgcolor='#12121f',
    font=dict(color='#cccccc', family='Malgun Gothic, sans-serif'),
    title=dict(font=dict(size=17, color='#ffffff'), x=0.5, xanchor='center'),
    xaxis=dict(showgrid=True, gridcolor='#222244',
               tickformat='%Y-%m-%d', tickangle=-30,
               title_font=dict(color='#aaaaaa')),
    yaxis=dict(showgrid=True, gridcolor='#222244',
               tickformat=',', title_font=dict(color='#aaaaaa')),
    hovermode='x unified',
    margin=dict(t=60, b=40, l=60, r=30),
)

COLORS = ['#e50914', '#ffd700', '#00cfff', '#ff7f50', '#90ee90']

# ─────────────────────────────────────────
# 데이터 로드
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
    selected_movie = st.selectbox("① 그래프에서 분석할 영화", movie_list)
    st.markdown("---")
    st.markdown(f"**총 영화 수:** {df['영화명'].nunique()}편")
    st.markdown(f"**기간:** {df['날짜'].min().strftime('%Y.%m.%d')} ~ {df['날짜'].max().strftime('%Y.%m.%d')}")
    st.markdown(f"**레코드 수:** {len(df):,}건")
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
    🎬 영화 데이터 그래프 도감
</h1>
<p style='text-align:center; color:#aaaaaa; margin-bottom:24px;'>
    영화진흥위원회 일별 박스오피스 데이터 분석
</p>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 1: 영화별 일관객 변화 추이
# ═════════════════════════════════════════
st.markdown('<div class="section-header">📈 1. 영화별 일관객 변화 추이</div>',
            unsafe_allow_html=True)

filtered_df = df[df['영화명'] == selected_movie].sort_values('날짜')

total_aud = int(filtered_df['일관객'].sum())
max_aud   = int(filtered_df['일관객'].max())
avg_aud   = int(filtered_df['일관객'].mean())
peak_date = filtered_df.loc[filtered_df['일관객'].idxmax(), '날짜'].strftime('%m/%d')

c1, c2, c3, c4 = st.columns(4)
c1.metric("🎟️ 누적 관객", f"{total_aud:,}명")
c2.metric("🏆 최고 일관객", f"{max_aud:,}명")
c3.metric("📊 평균 일관객", f"{avg_aud:,}명")
c4.metric("📅 최고 흥행일", peak_date)

fig1 = px.line(filtered_df, x='날짜', y='일관객',
               title=f"<b>'{selected_movie}'</b> 일별 관객수 추이",
               markers=True,
               labels={'날짜': '상영 날짜', '일관객': '일일 관객수 (명)'},
               color_discrete_sequence=['#e50914'])

peak_row = filtered_df.loc[filtered_df['일관객'].idxmax()]
fig1.add_scatter(
    x=[peak_row['날짜']], y=[peak_row['일관객']],
    mode='markers',
    marker=dict(size=14, color='#ffd700', symbol='star'),
    name='최고 흥행일',
    hovertemplate=f"최고 흥행일<br>{peak_row['날짜'].strftime('%Y-%m-%d')}<br>{int(peak_row['일관객']):,}명<extra></extra>"
)
fig1.update_traces(
    hovertemplate='날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>',
    selector=dict(mode='lines+markers')
)
fig1.update_layout(**CHART_LAYOUT,
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#333355', borderwidth=1))
st.plotly_chart(fig1, use_container_width=True)

with st.expander("📋 상세 데이터"):
    show1 = filtered_df[['날짜','일관객']].copy()
    show1['날짜']  = show1['날짜'].dt.strftime('%Y-%m-%d')
    show1['일관객'] = show1['일관객'].apply(lambda x: f"{int(x):,}명")
    st.dataframe(show1.rename(columns={'날짜':'상영 날짜','일관객':'일일 관객수'}),
                 use_container_width=True, hide_index=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 2: TOP 5 영화 비교
# ═════════════════════════════════════════
st.markdown('<div class="section-header">🏆 2. 흥행 TOP 5 영화 일관객 비교</div>',
            unsafe_allow_html=True)

top5 = (df.groupby('영화명')['일관객'].sum()
          .nlargest(5).reset_index())
top5_df = df[df['영화명'].isin(top5['영화명'])].sort_values('날짜')

medals = ['🥇','🥈','🥉','4위','5위']
cols   = st.columns(5)
for i, (_, row) in enumerate(top5.iterrows()):
    cols[i].metric(f"{medals[i]} {row['영화명']}", f"{int(row['일관객']):,}명")

fig2 = px.line(top5_df, x='날짜', y='일관객', color='영화명',
               title='<b>흥행 TOP 5</b> 일별 관객수 비교',
               labels={'날짜':'상영 날짜','일관객':'일일 관객수 (명)','영화명':'영화'},
               color_discrete_sequence=COLORS)
fig2.update_traces(
    hovertemplate='<b>%{fullData.name}</b><br>날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>',
    line=dict(width=2.5)
)
fig2.update_layout(**CHART_LAYOUT,
    legend=dict(
        title='🎬 영화 (클릭으로 켜기/끄기)',
        bgcolor='rgba(18,18,31,0.9)',
        bordercolor='#333355', borderwidth=1,
        itemclick='toggle', itemdoubleclick='toggleothers'
    )
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
<div class="info-box">
💡 범례를 <b>한 번 클릭</b>하면 해당 영화를 숨기거나 표시합니다.
<b>더블클릭</b>하면 해당 영화만 단독으로 볼 수 있어요.
</div>""", unsafe_allow_html=True)

with st.expander("📋 TOP 5 누적 관객 상세"):
    show2 = top5.copy()
    show2.index = medals
    show2.columns = ['영화명','누적 관객수']
    show2['누적 관객수'] = show2['누적 관객수'].apply(lambda x: f"{int(x):,}명")
    st.dataframe(show2, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 3: 날짜별 10위권 일관객 합계 영역 그래프
# ═════════════════════════════════════════
st.markdown('<div class="section-header">📅 3. 날짜별 박스오피스 10위권 일관객 합계</div>',
            unsafe_allow_html=True)

daily_sum = (df.groupby('날짜')['일관객']
               .sum()
               .reset_index()
               .rename(columns={'일관객':'일관객합계'})
               .sort_values('날짜'))

top3_days = daily_sum.nlargest(3, '일관객합계')

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=daily_sum['날짜'],
    y=daily_sum['일관객합계'],
    mode='lines',
    fill='tozeroy',
    fillcolor='rgba(229,9,20,0.2)',
    line=dict(color='#e50914', width=2),
    hovertemplate='날짜: %{x|%Y-%m-%d}<br>합계 관객: %{y:,}명<extra></extra>',
    name='10위권 합계'
))
fig3.add_trace(go.Scatter(
    x=top3_days['날짜'],
    y=top3_days['일관객합계'],
    mode='markers+text',
    marker=dict(size=13, color='#ffd700', symbol='star',
                line=dict(color='#ffffff', width=1)),
    text=top3_days['날짜'].dt.strftime('%m/%d'),
    textposition='top center',
    textfont=dict(color='#ffd700', size=12),
    hovertemplate='<b>🏆 %{x|%Y-%m-%d}</b><br>합계 관객: %{y:,}명<extra></extra>',
    name='Top 3일'
))

# ✅ CHART_LAYOUT 대신 필요한 항목만 직접 지정
fig3.update_layout(
    plot_bgcolor='#12121f',
    paper_bgcolor='#12121f',
    font=dict(color='#cccccc', family='Malgun Gothic, sans-serif'),
    title=dict(
        text='<b>날짜별 박스오피스 10위권 일관객 합계</b>',
        font=dict(size=17, color='#ffffff'),
        x=0.5, xanchor='center'
    ),
    xaxis=dict(
        showgrid=True, gridcolor='#222244',
        tickformat='%Y-%m-%d', tickangle=-30,   # 날짜 형식 명시
        title='날짜', title_font=dict(color='#aaaaaa')
    ),
    yaxis=dict(
        showgrid=True, gridcolor='#222244',
        tickformat=',',
        title='일관객 합계 (명)', title_font=dict(color='#aaaaaa')
    ),
    hovermode='x unified',
    margin=dict(t=60, b=40, l=60, r=30),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#333355', borderwidth=1)
)
    )

st.markdown("""
<div class="info-box">
💡 황금연휴·명절·방학 시즌에 전체 박스오피스 관객이 급증하는 패턴을 확인할 수 있습니다.
⭐ 별 마커가 표시된 날이 기간 내 가장 많은 관객이 든 Top 3일입니다.
</div>""", unsafe_allow_html=True)

with st.expander("📋 날짜별 합계 상세 데이터"):
    show3 = daily_sum.copy()
    show3['날짜']      = show3['날짜'].dt.strftime('%Y-%m-%d')
    show3['일관객합계'] = show3['일관객합계'].apply(lambda x: f"{int(x):,}명")
    st.dataframe(show3.rename(columns={'일관객합계':'10위권 관객 합계'}),
                 use_container_width=True, hide_index=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 4: 흥행 TOP 10 가로 막대 그래프
# ═════════════════════════════════════════
st.markdown('<div class="section-header">🎖️ 4. 흥행 TOP 10 영화 누적 관객 순위</div>',
            unsafe_allow_html=True)

# TOP 10 집계 + 10위권 등재 날수 계산
top10 = (df.groupby('영화명')['일관객']
           .sum()
           .nlargest(10)
           .reset_index()
           .rename(columns={'일관객':'누적관객'}))

# 10위권에 든 날수 = 해당 영화가 데이터에 등장한 행 수
days_in_top10 = (df.groupby('영화명')
                   .size()
                   .reset_index(name='10위권날수'))

top10 = top10.merge(days_in_top10, on='영화명')

# 관객 많은 영화가 위에 오도록 오름차순 정렬 (Plotly 가로 막대는 아래→위)
top10_sorted = top10.sort_values('누적관객', ascending=True)

fig4 = go.Figure()
fig4.add_trace(go.Bar(
    x=top10_sorted['누적관객'],
    y=top10_sorted['영화명'],
    orientation='h',                          # 가로 막대
    marker=dict(
        color=top10_sorted['누적관객'],        # 값 크기에 따라 색상 그라데이션
        colorscale=[
            [0,   '#7b0000'],
            [0.5, '#e50914'],
            [1,   '#ffd700'],
        ],
        showscale=False,
    ),
    # 마우스 오버 툴팁: 누적 관객 + 10위권 날수
    customdata=top10_sorted['10위권날수'],
    hovertemplate=(
        '<b>%{y}</b><br>'
        '누적 관객: %{x:,}명<br>'
        '10위권 등재 날수: %{customdata}일'
        '<extra></extra>'
    ),
    text=top10_sorted['누적관객'].apply(lambda x: f"{int(x):,}명"),
    textposition='outside',
    textfont=dict(color='#cccccc', size=11),
))

fig4.update_layout(
    **{k: v for k, v in CHART_LAYOUT.items()
       if k not in ('xaxis', 'yaxis', 'hovermode')},   # 기본 레이아웃 재사용
    title='<b>흥행 TOP 10</b> 누적 관객수',
    xaxis=dict(
        showgrid=True, gridcolor='#222244',
        tickformat=',', title='누적 관객수 (명)',
        title_font=dict(color='#aaaaaa'),
    ),
    yaxis=dict(
        showgrid=False, title='',
        tickfont=dict(size=12, color='#ffffff'),
        automargin=True,
    ),
    hovermode='y unified',
    margin=dict(t=60, b=40, l=160, r=100),
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
<div class="info-box">
💡 막대에 마우스를 올리면 <b>누적 관객수</b>와 함께
해당 영화가 <b>10위권에 든 날수</b>를 확인할 수 있습니다.
색이 밝을수록 누적 관객이 많은 영화입니다.
</div>""", unsafe_allow_html=True)

with st.expander("📋 TOP 10 상세 데이터"):
    show4 = top10_sorted.sort_values('누적관객', ascending=False).copy()
    show4.index = range(1, 11)
    show4['누적관객']    = show4['누적관객'].apply(lambda x: f"{int(x):,}명")
    show4['10위권날수'] = show4['10위권날수'].apply(lambda x: f"{x}일")
    show4.columns = ['영화명', '누적 관객수', '10위권 등재 날수']
    st.dataframe(show4, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ═════════════════════════════════════════
# 섹션 5: 월 × 요일별 일관객 합계 히트맵
# ═════════════════════════════════════════
st.markdown('<div class="section-header">🗓️ 5. 월 × 요일별 일관객 합계 히트맵</div>',
            unsafe_allow_html=True)

# 월·요일 파생 컬럼 생성
heatmap_df = df.copy()
heatmap_df['월']  = heatmap_df['날짜'].dt.month
heatmap_df['요일'] = heatmap_df['날짜'].dt.dayofweek   # 0=월 ~ 6=일

# 월×요일별 합계 피벗
pivot = (heatmap_df.groupby(['월','요일'])['일관객']
                   .sum()
                   .reset_index()
                   .pivot(index='요일', columns='월', values='일관객'))

# 요일 레이블 (월→일 순서)
DAY_LABELS = ['월','화','수','목','금','토','일']
# 월 레이블
month_labels = [f"{m}월" for m in pivot.columns]

fig5 = go.Figure(data=go.Heatmap(
    z=pivot.values,
    x=month_labels,
    y=DAY_LABELS,
    colorscale=[
        [0,    '#0f0f1a'],   # 가장 어두운 색 (관객 적음)
        [0.25, '#7b0000'],
        [0.6,  '#e50914'],
        [1,    '#ffd700'],   # 가장 밝은 색 (관객 많음)
    ],
    hovertemplate='%{x} %{y}요일<br>일관객 합계: %{z:,}명<extra></extra>',
    showscale=True,
    colorbar=dict(
        title='일관객 합계',
        tickformat=',',
        titlefont=dict(color='#aaaaaa'),
        tickfont=dict(color='#aaaaaa'),
    ),
))

fig5.update_layout(
    title='<b>월 × 요일별</b> 일관객 합계',
    paper_bgcolor='#12121f',
    plot_bgcolor='#12121f',
    font=dict(color='#cccccc', family='Malgun Gothic, sans-serif'),
    title_font=dict(size=17, color='#ffffff'),
    title_x=0.5,
    xaxis=dict(title='월', title_font=dict(color='#aaaaaa'),
               tickfont=dict(size=12)),
    yaxis=dict(title='요일', title_font=dict(color='#aaaaaa'),
               tickfont=dict(size=13),
               autorange='reversed'),   # 월요일이 위에 오도록
    margin=dict(t=60, b=40, l=60, r=60),
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
<div class="info-box">
💡 <b>색이 진할수록 관객이 많습니다.</b>
주말(토·일)과 특정 월(여름·겨울 방학, 명절 연휴 등)에 관객이 집중되는 패턴을 읽어보세요.
가로축(월)과 세로축(요일)을 함께 보면 언제 영화관이 가장 붐비는지 알 수 있습니다.
</div>""", unsafe_allow_html=True)

with st.expander("📋 월×요일 합계 상세 데이터"):
    show5 = pivot.copy()
    show5.index   = DAY_LABELS
    show5.columns = month_labels
    show5 = show5.applymap(lambda x: f"{int(x):,}명" if pd.notna(x) else "-")
    st.dataframe(show5, use_container_width=True)
