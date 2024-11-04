import pandas as pd
import streamlit as st
import plotly.express as px
import requests

# Define the server URL
SERVER_URL = "http://127.0.0.1:5000"

st.write(""" 
         # DataSUS - Sinan - Comparações entre Doenças    
         """)

# Add a multiselect to filter dataframes
dfs_option = st.multiselect(
    'Selecione Dataframes',
    options=['ZIKA', 'CHIK', 'DENG', 'AIDS'],
    default=['ZIKA', 'CHIK', 'AIDS']
)

# Add a selectbox to select frequency
frequency_option = st.selectbox(
    'Selecione a Frequência',
    options=['ME', 'D', 'W', 'YE'],
    format_func=lambda x: 'Diário' if x == 'D' else 'Semanal' if x == 'W' else 'Mensal' if x == 'ME' else 'Anual'
)

# Add a slider to select time period
start_date, end_date = st.slider(
    'Selecione o Período de Tempo',
    min_value=pd.to_datetime('2016-01-01').date(),
    max_value=pd.to_datetime('2023-12-31').date(),
    value=(pd.to_datetime('2016-01-01').date(), pd.to_datetime('2023-12-31').date())
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

@st.cache_data
def get_combined_df(dfs_option, start_date, end_date, sexo_option, raca_option, idade_option, frequency_option):

    headers = {
        'dfs-option': ','.join(dfs_option),
        'start-date': str(start_date),
        'end-date': str(end_date),
        'sexo-option': str(sexo_option),
        'raca-option': str(raca_option),
        'idade-option': ','.join(map(str, idade_option)),
        'frequency-option': frequency_option
    }
    response = requests.get(f"{SERVER_URL}/get_combined_df", headers=headers)
    if response.status_code == 200:
        combined_df = pd.read_json(response.text, orient='split')
        return combined_df
    else:
        st.error("Failed to fetch data from the server")
        return pd.DataFrame()
    
combined_df = get_combined_df(dfs_option, start_date, end_date, sexo_option, raca_option, idade_option, frequency_option)

if not combined_df.empty:
    # Plot data
    fig = px.line(combined_df, x=combined_df.index, y='casos', color='doenca', title='Casos por Doença')
    st.plotly_chart(fig, key=1)