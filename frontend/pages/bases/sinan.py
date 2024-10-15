import pandas as pd
import streamlit as st
import plotly.express as px

col = st.columns(2, gap="small", vertical_alignment="top")

df_zika = pd.read_csv('data/sinan/zika_serie_anual.csv')
df_aids = pd.read_csv('data/sinan/aids_serie_anual.csv')
df_chik = pd.read_csv('data/sinan/chik_serie_anual.csv')
df_deng = pd.read_csv('data/sinan/dengue_serie_anual.csv')

with st.container():
    with col[0]:
        st.plotly_chart(px.line(df_zika, x='ANO', y='CASOS', title='Casos de zika por ano'), key=1)

    with col[1]:
        st.plotly_chart(px.line(df_aids, x='ANO', y='CASOS', title='Casos de AIDS por ano'), key=2)

with st.container():
    with col[0]:
        st.plotly_chart(px.line(df_chik, x='ANO', y='CASOS', title='Casos de chikungunya por ano'), key=4)

    with col[1]:
        st.plotly_chart(px.line(df_deng, x='ANO', y='CASOS', title='Casos de dengue por ano'), key=3)

