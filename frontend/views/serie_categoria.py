import streamlit as st
import plotly.express as px
import pandas as pd
from global_values import *


st.write(""" 
         # DataSUS - Sinan - Comparações entre Valores de Categoria    
         """)

start_date=pd.to_datetime('2016-01-01').date()
end_date=pd.to_datetime('2023-12-31').date()

# Add a multiselect to filter dataframes
dfs_option = st.multiselect(
    'Selecione Dataframes',
    #options=['ZIKA', 'CHIK', 'DENG', 'AIDS'],
    #default=['ZIKA', 'CHIK', 'DENG', 'AIDS']
    options=['ZIKA', 'CHIK', 'AIDS'],
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
        return sex_codes.keys()
    elif column == 'raca':
        return skin_color_codes.keys()
    elif column == 'estado':
        return uf_codes.keys()

values_options = st.multiselect(
    'Selecione os Valores para Comparar',
    options=get_values(column_option),
    default=[]
)

@st.cache_data
def get_dfs_to_plot(dfs_option, column_option, values_options):

    def load_data():
        df_zika = pd.read_parquet('frontend/data/ZIKA.parquet')
        df_chik = pd.read_parquet('frontend/data/CHIK.parquet')
        #df_deng = pd.read_parquet('data/DENG.parquet')
        df_deng = None
        df_aids = pd.read_parquet('frontend/data/AIDS.parquet')
        return df_zika, df_chik, df_deng, df_aids
    
    def process_df(df, column_option, values_trasformed):
        df = df[(df.index.date >= start_date) & (df.index.date <= end_date)]
        df = df[[column_option]]

        df[column_option] = df[column_option].apply(lambda x: x if x in values_trasformed else None)
        df = pd.get_dummies(df, columns=[column_option], prefix="", prefix_sep="")
        df.columns = df.columns.astype(float).astype(int)

        df = df.resample('ME').sum()
        df = df.rename(columns = get_inverted_dict(column_option))

        df = df.reset_index()
        df = pd.melt(df, id_vars=['data'], var_name='categoria', value_name='casos')
        df = df.set_index('data')

        return df
    
    def get_values_transformed(column, values):
        if column == 'sexo':
            return  [sex_codes[value] for value in values]
        elif column == 'raca':
            return [skin_color_codes[value] for value in values]
        elif column == 'estado':
            return [uf_codes[value] for value in values]
        
    def get_inverted_dict(column):
        if column == 'sexo':
            return inverted_sex_codes
        elif column == 'raca':
            return inverted_skin_color_codes
        elif column == 'estado':
            return inverted_uf_codes

    df_zika, df_chik, df_deng, df_aids = load_data()

    df_dict = {
        'ZIKA': df_zika,
        'CHIK': df_chik,
        'AIDS': df_aids,
        'DENG': df_deng
    }

    values_trasformed = get_values_transformed(column_option, values_options)

    dfs_to_plot = []

    for disease in dfs_option:
        df = df_dict[disease]
        df = process_df(df, column_option, values_trasformed)
        dfs_to_plot.append((df, disease))

    return dfs_to_plot


for df, disease in get_dfs_to_plot(dfs_option, column_option, values_options):
    # Create a seasonal plot
    fig = px.line(df, x=df.index, y='casos', color='categoria', title=f'Casos de {disease} por {column_option}')

    # Display the plot in Streamlit
    st.plotly_chart(fig)

