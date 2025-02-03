import streamlit as st
import pandas as pd
import sqlite3
import os

def resout(sdata, squer1):
    if len(sdata)>=3:
        ## DB 연결
        squer2 = '%' + sdata + '%'
        con = sqlite3.connect('DB/IMSDATA2024.db')
        dfa = pd.read_sql('SELECT * FROM DATA WHERE "%s" LIKE "%s"' % (squer1, squer2), con, index_col='index')
        if dfa.shape[0] == 0:
            st.write('검색결과가 없습니다.')
        else:
            ## 매출 표시
            dfa2 = pd.DataFrame({'MAT20Q3':[dfa['MAT20Q3'].sum()],'MAT21Q3':[dfa['MAT21Q3'].sum()],'MAT22Q3':[dfa['MAT22Q3'].sum()],
                                 'MAT23Q3':[dfa['MAT23Q3'].sum()],'MAT24Q3':[dfa['MAT24Q3'].sum()]})
            st.write('･연도별 총 매출')
            st.dataframe(dfa2, hide_index=1)

            ## 용량별 매출
            a = dfa.groupby('용량')
            st.write('･용량별 매출')
            st.write('\n', a.sum().iloc[0:, 42:47])

            st.write('･연도별 매출 그래프')
            st.bar_chart(a.sum().iloc[0, 42:47])

            st.write('･제품별 매출')
            st.dataframe(dfa[['Audit desc.','제품명','성분명','용량','급여구분','MAT20Q3','MAT21Q3','MAT22Q3','MAT23Q3','MAT24Q3']])

            ## DB 닫기
            con.commit()
            con.close()
    else:
        st.write('3글자 이상 입력해 주세요.')


## 페이지 레이아웃
st.set_page_config(layout="wide")
st.sidebar.header('검색')
srn = ['성분명','제품명']
ssrn = st.sidebar.selectbox('검색 유형을 선택하세요', srn)
name = st.sidebar.text_input(label="검색어를 입력해주세요")
resout(name, ssrn)

upload_file = st.sidebar.file_uploader('DB업로드')
out2 = st.empty()

if upload_file:
    if not os.path.exists('DB'):
        os.makedirs('DB')
    with open(os.path.join('DB', upload_file.name), 'wb') as f:
        f.write(upload_file.getbuffer())
    con3 = sqlite3.connect('DB/'+upload_file.name)
    df2 = pd.read_sql("SELECT * FROM DATA", con3, index_col='index')
    st.write(df2)
    con3.close()