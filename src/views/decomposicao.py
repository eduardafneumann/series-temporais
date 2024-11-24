import streamlit as st
import plotly.express as px
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt


st.write(""" 
         # DataSUS - Sinan - Decomposição das Séries
         """)

start_date=pd.to_datetime('2016-01-01').date()
end_date=pd.to_datetime('2023-12-31').date()

@st.cache_data
def load_data():
    df_zika = pd.read_parquet('data/ZIKA.parquet')
    df_chik = pd.read_parquet('data/CHIK.parquet')
    #df_deng = pd.read_parquet('data/DENG.parquet')
    df_deng = None
    df_aids = pd.read_parquet('data/AIDS.parquet')
    return df_zika, df_chik, df_deng, df_aids

df_zika, df_chik, df_deng, df_aids = load_data()

df_option = st.selectbox(
    'Selecione a série',
    options=['ZIKA', 'CHIK', 'AIDS']
)

szn_option = st.selectbox(
    'Selecione a sazonalidade',
    options=['Semanal', 'Mensal', 'Anual']
)

if df_option == 'ZIKA':
    df = df_zika
elif df_option == 'CHIK':
    df = df_chik
elif df_option == 'AIDS':
    df = df_aids

if szn_option == 'Semanal':
    szn = 7
elif szn_option == 'Mensal':
    szn = 30
elif szn_option == 'Anual':
    szn = 365

df_cases_count = df.groupby('data').size().reset_index(name='Number of Cases')

results = seasonal_decompose(df_cases_count['Number of Cases'], period=szn)

df_observed = pd.DataFrame({'Casos' : results.observed, "Tempo" : df_cases_count['data']})
fig = px.line(df_observed, 
              title = "Série observada",
              x=df_observed['Tempo'],
              y=df_observed['Casos']
)
st.plotly_chart(fig)

df_trend = pd.DataFrame({'Casos' : results.trend, "Tempo" : df_cases_count['data']})
fig = px.line(df_trend, 
              title = "Tendência da série",
              x=df_trend['Tempo'],
              y=df_trend['Casos']
)
st.plotly_chart(fig)

df_seasonal = pd.DataFrame({'Casos' : results.seasonal, "Tempo" : df_cases_count['data']})
fig = px.line(df_seasonal, 
              title = "Sazonalidade da série",
              x=df_seasonal['Tempo'],
              y=df_seasonal['Casos']
)
st.plotly_chart(fig)

df_resid = pd.DataFrame({'Casos' : results.resid, "Tempo" : df_cases_count['data']})
fig = px.line(df_resid, 
              title = "Resíduo",
              x=df_resid['Tempo'],
              y=df_resid['Casos']
)
st.plotly_chart(fig)
