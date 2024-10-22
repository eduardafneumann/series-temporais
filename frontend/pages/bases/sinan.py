import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df_zika = pd.read_parquet('data-extraction/parquet_data/ZIKA.parquet')
    df_chik = pd.read_parquet('data-extraction/parquet_data/CHIK.parquet')
    df_deng = pd.read_parquet('data-extraction/parquet_data/DENG.parquet')
    df_aids = pd.read_parquet('data-extraction/parquet_data/AIDS.parquet')
    return df_zika, df_chik, df_deng, df_aids

df_zika, df_chik, df_deng, df_aids = load_data()

# Add a multiselect box for selecting dataframes
dfs_option = st.multiselect(
    'Select Dataframes',
    options=['ZIKA', 'CHIK', 'DENG', 'AIDS'],
    default=['ZIKA', 'CHIK', 'DENG', 'AIDS']
)

# Add a slider for selecting the time period
start_date, end_date = st.slider(
    'Select Time Period',
    min_value=pd.to_datetime('2000-01-01').date(),
    max_value=pd.to_datetime('2023-12-31').date(),
    value=(pd.to_datetime('2020-01-01').date(), pd.to_datetime('2023-12-31').date())
)

# Add a selectbox for filtering by "sexo"
sexo_option = st.selectbox(
    'Select Gender',
    options=[-1, 0, 1, 2],
    format_func=lambda x: 'All' if x == -1 else 'Not Identified' if x == 0 else 'Male' if x == 1 else 'Female'
)

# Add a selectbox for filtering by "raca"
raca_option = st.selectbox(
    'Select Race',
    options=[-1, 0, 1, 2, 3, 4, 5],
    format_func=lambda x: 'All' if x == -1 else 'Not Identified' if x == 0 else 'White' if x == 1 else 'Black' if x == 2 else 'Yellow' if x == 3 else 'Brown' if x == 4 else 'Indigenous'
)

# Add a slider for filtering by "idade"
idade_option = st.slider(
    'Select Age',
    min_value=0,
    max_value=150,
    value=(0, 150)
)

# Function to filter dataframe by time
@st.cache_data
def filter_df_time(df, start_date, end_date):
    return df[(df.index.date >= start_date) & (df.index.date <= end_date)]


# Function to filter dataframe
def filter_df(df, start_date, end_date, sexo_option, raca_option, idade_option, disease):
    df = filter_df_time(df, start_date, end_date)
    if sexo_option != -1:
        df = df[df['sexo'] == sexo_option]
    if raca_option != -1:
        df = df[df['raca'] == raca_option]
    df = df[(df['idade'] >= idade_option[0]) & (df['idade'] <= idade_option[1])]


    df = df.resample('D').count()
    df = df[['sexo']]
    df = df.rename(columns={'sexo': 'casos'})
    df['doenca'] = disease

    return df

# Filter selected dataframes
filtered_dfs = []
if 'ZIKA' in dfs_option:
    filtered_dfs.append(filter_df(df_zika, start_date, end_date, sexo_option, raca_option, idade_option, 'ZIKA'))
if 'CHIK' in dfs_option:
    filtered_dfs.append(filter_df(df_chik, start_date, end_date, sexo_option, raca_option, idade_option, 'CHIK'))
if 'DENG' in dfs_option:
    filtered_dfs.append(filter_df(df_deng, start_date, end_date, sexo_option, raca_option, idade_option, 'DENG'))
if 'AIDS' in dfs_option:
    filtered_dfs.append(filter_df(df_aids, start_date, end_date, sexo_option, raca_option, idade_option, 'AIDS'))

# Combine filtered dataframes
if filtered_dfs:
    combined_df = pd.concat(filtered_dfs)
    
    # Plot line chart for the combined data
    fig = px.line(combined_df, x=combined_df.index, y='casos', color='doenca', title='Casos por Doença')
    st.plotly_chart(fig, key=1)