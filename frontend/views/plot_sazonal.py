import streamlit as st
import plotly.express as px
import pandas as pd


st.write(""" 
         # DataSUS - Sinan - Plots Sazonais    
         """)

start_date=pd.to_datetime('2016-01-01').date()
end_date=pd.to_datetime('2023-12-31').date()

# Load data
@st.cache_data
def load_data():
    df_zika = pd.read_parquet('frontend/data/ZIKA.parquet')
    df_chik = pd.read_parquet('frontend/data/CHIK.parquet')
    #df_deng = pd.read_parquet('data/DENG.parquet')
    df_deng = None
    df_aids = pd.read_parquet('frontend/data/AIDS.parquet')
    return df_zika, df_chik, df_deng, df_aids


df_zika, df_chik, df_deng, df_aids = load_data()

# Add a multiselect to filter dataframes
dfs_option = st.multiselect(
    'Selecione Dataframes',
    #options=['ZIKA', 'CHIK', 'DENG', 'AIDS'],
    #default=['ZIKA', 'CHIK', 'DENG', 'AIDS']
    options=['ZIKA', 'CHIK', 'AIDS'],
    default=['ZIKA', 'CHIK', 'AIDS']
)

df_dict = {
    'ZIKA': df_zika,
    'CHIK': df_chik,
    'AIDS': df_aids,
    'DENG': df_deng
}

for disease in dfs_option:
    df = df_dict[disease]
    df = df[(df.index.date >= start_date) & (df.index.date <= end_date)]
    df = df.resample('ME').count()
    df = df[['sexo']].rename(columns={'sexo': 'casos'})

    df['ano'] = df.index.year
    df['mes'] = df.index.month_name()

    # Create a seasonal plot
    fig = px.line(df, x='mes', y='casos', color='ano', title=f'Plot Sazonal de {disease}')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

