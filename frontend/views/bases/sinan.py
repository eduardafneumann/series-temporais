import pandas as pd
import streamlit as st
import plotly.express as px

st.write(""" 
         # DataSUS - Sinan         
         """)

# Load data
@st.cache_data
def load_data():
    df_zika = pd.read_parquet('data-extraction/parquet_data/ZIKA.parquet')
    df_chik = pd.read_parquet('data-extraction/parquet_data/CHIK.parquet')
    #df_deng = pd.read_parquet('data-extraction/parquet_data/DENG.parquet')
    df_deng = None
    df_aids = pd.read_parquet('data-extraction/parquet_data/AIDS.parquet')
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

# Add a selectbox to select frequency
frequency_option = st.selectbox(
    'Selecione a Frequência',
    options=['D', 'W', 'YE'],
    format_func=lambda x: 'Diário' if x == 'D' else 'Semanal' if x == 'W' else 'Anual'
)

# Add a slider to select time period
start_date, end_date = st.slider(
    'Selecione o Período de Tempo',
    min_value=pd.to_datetime('2000-01-01').date(),
    max_value=pd.to_datetime('2023-12-31').date(),
    value=(pd.to_datetime('2020-01-01').date(), pd.to_datetime('2023-12-31').date())
)

# Add a selectbox to filter by "sexo"
sexo_option = st.selectbox(
    'Selecione o Gênero',
    options=[-1, 0, 1, 2],
    format_func=lambda x: 'Todos' if x == -1 else 'Não Identificado' if x == 0 else 'Masculino' if x == 1 else 'Feminino'
)

# Add a selectbox to filter by "raca"
raca_option = st.selectbox(
    'Selecione a Raça',
    options=[-1, 0, 1, 2, 3, 4, 5],
    format_func=lambda x: 'Todos' if x == -1 else 'Não Identificado' if x == 0 else 'Branca' if x == 1 else 'Preta' if x == 2 else 'Amarela' if x == 3 else 'Parda' if x == 4 else 'Indígena'
)

# Add a slider to select age
idade_option = st.slider(
    'Selecione a Idade',
    min_value=0,
    max_value=150,
    value=(0, 150)
)

# Function to filter dataframe by time
@st.cache_data
def filter_df_time(df, start_date, end_date):
    return df[(df.index.date >= start_date) & (df.index.date <= end_date)]

# Function to filter dataframe
def filter_df(df, start_date, end_date, sexo_option, raca_option, idade_option, disease, frequency):
    df = filter_df_time(df, start_date, end_date)
    if sexo_option != -1:
        df = df[df['sexo'] == sexo_option]
    if raca_option != -1:
        df = df[df['raca'] == raca_option]
    df = df[(df['idade'] >= idade_option[0]) & (df['idade'] <= idade_option[1])]

    df = df.resample(frequency).count()
    df = df[['sexo']]
    df = df.rename(columns={'sexo': 'casos'})
    df['doenca'] = disease

    return df

# Filter selected dataframes
filtered_dfs = []
if 'ZIKA' in dfs_option:
    filtered_dfs.append(filter_df(df_zika, start_date, end_date, sexo_option, raca_option, idade_option, 'ZIKA', frequency_option))
if 'CHIK' in dfs_option:
    filtered_dfs.append(filter_df(df_chik, start_date, end_date, sexo_option, raca_option, idade_option, 'CHIK', frequency_option))
if 'DENG' in dfs_option:
    filtered_dfs.append(filter_df(df_deng, start_date, end_date, sexo_option, raca_option, idade_option, 'DENG', frequency_option))
if 'AIDS' in dfs_option:
    filtered_dfs.append(filter_df(df_aids, start_date, end_date, sexo_option, raca_option, idade_option, 'AIDS', frequency_option))

# Combine filtered dataframes
if filtered_dfs:
    combined_df = pd.concat(filtered_dfs)
    
    # Plot data
    fig = px.line(combined_df, x=combined_df.index, y='casos', color='doenca', title='Casos por Doença')
    st.plotly_chart(fig, key=1)