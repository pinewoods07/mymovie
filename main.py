import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="영화 데이터 그래프 도감", layout="wide")

st.title("영화 데이터 그래프 도감 1 - 시간")
st.markdown("영화진흥위원회 1년치 일별 박스오피스 데이터를 분석합니다.")

# 1. 데이터 불러오기 및 전처리 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    # 한글 인코딩 처리 및 데이터 로드
    df = pd.read_csv(url, encoding='utf-8')
    
    # 여덟 자리 숫자 형태의 날짜(YYYYMMDD)를 실제 datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

df = load_data()

st.divider()

# 2. 첫 번째 그래프 구역: 영화별 일일 관객수 추이
with st.container():
    st.header("1. 영화별 일관객 변화 추이")
    
    # 영화 선택 드롭다운
    movie_list = df['영화명'].unique()
    selected_movie = st.selectbox("그래프로 확인할 영화를 선택하세요:", movie_list)
    
    # 선택한 영화 데이터만 필터링
    filtered_df = df[df['영화명'] == selected_movie]
    
    # 플롯리(Plotly) 선 그래프 생성
    fig = px.line(
        filtered_df, 
        x='날짜', 
        y='일관객',
        title=f"'{selected_movie}' 일별 관객수",
        markers=True, # 데이터 포인트에 마커 표시
        labels={'날짜': '상영 날짜', '일관객': '일일 관객수 (명)'}
    )
    
    # 마우스 오버(Hover) 툴팁 설정
    fig.update_traces(hovertemplate='<b>날짜</b>: %{x}<br><b>관객수</b>: %{y:,}명<extra></extra>')
    
    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 분석 문구 자리
    st.info("💡 **이 그래프로 알 수 있는 것:** 개봉 첫 주말에 관객이 가장 많이 몰리며, 이후 점진적으로 감소하는 일반적인 흥행 패턴을 보입니다.")

st.divider()

# 3. 추가 그래프를 위한 빈 구역 (향후 확장용)
with st.container():
    st.header("2. (새로운 그래프 제목을 입력하세요)")
    st.write("이곳에 다음 그래프와 코드를 추가할 수 있습니다.")
    st.info("💡 **이 그래프로 알 수 있는 것:** (추가 예정)")
