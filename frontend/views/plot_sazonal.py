import streamlit as st
import plotly.express as px
import requests
import pandas as pd

# Define the server URL
SERVER_URL = "http://127.0.0.1:5000"

@st.cache_data
def get_dfs_to_plot(dfs_option, start_date, end_date):

    headers = {
        'dfs-option': ','.join(dfs_option),
        'start-date': str(start_date),
        'end-date': str(end_date)
    }
    response = requests.get(f"{SERVER_URL}/get_dfs_to_plot_sazonal", headers=headers)
    if response.status_code == 200:
        data = response.json()
        dfs_to_plot = [(pd.read_json(data[disease], orient='split'), disease) for disease in data]
        return dfs_to_plot
    else:
        st.error("Failed to fetch data from the server")
        return []

st.write(""" 
         # DataSUS - Sinan - Plots Sazonais    
         """)

start_date=pd.to_datetime('2016-01-01').date()
end_date=pd.to_datetime('2023-12-31').date()

# Add a multiselect to filter dataframes
dfs_option = st.multiselect(
    'Selecione Dataframes',
    options=['ZIKA', 'CHIK', 'DENG', 'AIDS'],
    default=['ZIKA', 'CHIK', 'AIDS']
)

dfs_to_plot = get_dfs_to_plot(dfs_option, start_date, end_date)

for df, disease in dfs_to_plot:
    # Create a seasonal plot
    fig = px.line(df, x='mes', y='casos', color='ano', title=f'Plot Sazonal de {disease}')

    # Display the plot in Streamlit
    st.plotly_chart(fig)