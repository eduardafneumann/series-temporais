import streamlit as st
import pandas as pd
import plotly.express as px
from global_values import *
import requests

# Define the server URL
SERVER_URL = "http://127.0.0.1:5000"

st.write(""" 
         # DataSUS - Sinan - Comparações entre Valores de Categoria    
         """)

start_date = pd.to_datetime('2016-01-01').date()
end_date = pd.to_datetime('2023-12-31').date()

# Add a multiselect to filter dataframes
dfs_option = st.multiselect(
    'Selecione Dataframes',
    options=['ZIKA', 'CHIK', 'AIDS', 'DENG'],
    default=['ZIKA', 'CHIK', 'AIDS']
)

# Add a dropdown to select columns to display
column_option = st.selectbox(
    'Selecione a Coluna para Visualizar',
    options=['sexo', 'raca', 'estado'],
    index=0
)

def get_values(column):
    if column == 'sexo':
        return list(sex_codes.keys())
    elif column == 'raca':
        return list(skin_color_codes.keys())
    elif column == 'estado':
        return list(uf_codes.keys())

values_options = st.multiselect(
    'Selecione os Valores para Comparar',
    options=get_values(column_option),
    default=[]
)

# Function to get data from the server
def get_dfs_to_plot(dfs_option, column_option, values_options):
    headers = {
        'dfs-option': ','.join(dfs_option),
        'column-option': column_option,
        'values-options': ','.join(values_options),
        'start-date': str(start_date),
        'end-date': str(end_date)
    }
    response = requests.get(f"{SERVER_URL}/get_dfs_to_plot_categoria", headers=headers)
    if response.status_code == 200:
        data = response.json()
        dfs_to_plot = [(pd.read_json(data[disease], orient='split'), disease) for disease in data]
        return dfs_to_plot
    else:
        st.error("Failed to fetch data from the server")
        return []

dfs_to_plot = get_dfs_to_plot(dfs_option, column_option, values_options)

for df, disease in dfs_to_plot:
    # Create a plot for the category comparison
    fig = px.line(df, x=df.index, y='casos', color='categoria', title=f'Comparação de {column_option} para {disease}')

    # Display the plot in Streamlit
    st.plotly_chart(fig)