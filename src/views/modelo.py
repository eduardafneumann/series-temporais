import pandas as pd
import streamlit as st
import plotly.express as px

st.write(""" 
         # DataSUS - Sinan - Modelagem    
         """)

# Load data
@st.cache_data
def load_data():
    df_zika = pd.read_parquet('data/ZIKA.parquet')
    df_chik = pd.read_parquet('data/CHIK.parquet')
    #df_deng = pd.read_parquet('data/DENG.parquet')
    df_deng = None
    df_aids = pd.read_parquet('data/AIDS.parquet')
    return df_zika, df_chik, df_deng, df_aids

df_zika, df_chik, df_deng, df_aids = load_data()

# Add a selectbox to select a dataframe
df_option = st.selectbox(
    'Selecione DataFrame da série que quer modelar',
    options=['ZIKA', 'CHIK', 'AIDS']
)

if df_option == 'ZIKA':
    df = df_zika
elif df_option == 'CHIK':
    df = df_chik
elif df_option == 'AIDS':
    df = df_aids

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

# Select a model
model_option = st.selectbox(
    'Selecione o Modelo',
    options=['SARIMA', 'ARIMA', 'AR']
)

# Function to filter dataframe by time
@st.cache_data
def filter_df_time(df, start_date, end_date):
    return df[(df.index.date >= start_date) & (df.index.date <= end_date)]

# Function to filter dataframe
@st.cache_data
def filter_df(df, start_date, end_date, sexo_option, raca_option, idade_option):
    df = filter_df_time(df, start_date, end_date)
    if sexo_option != -1:
        df = df[df['sexo'] == sexo_option]
    if raca_option != -1:
        df = df[df['raca'] == raca_option]
    df = df[(df['idade'] >= idade_option[0]) & (df['idade'] <= idade_option[1])]

    df = df.resample('D').count()
    df = df[['sexo']].rename(columns={'sexo': 'casos'})

    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df = df.reindex(all_dates, fill_value=0)
    df.index.name = 'date'

    return df

# Filter selected temporal series to model
filtered_df = filter_df(df_zika, start_date, end_date, sexo_option, raca_option, idade_option)

train_size = int(len(filtered_df) * 0.8)
test_size = len(filtered_df) - train_size

train_df = filtered_df.iloc[:train_size]
test_df = filtered_df.iloc[train_size:]

if model_option == 'AR':
    # Fit AR model
    from statsmodels.tsa.ar_model import AutoReg

    model = AutoReg(train_df, lags=1)
    model_fit = model.fit()

    # Forecast
    forecast = model_fit.predict(start=len(train_df), end=len(train_df) + len(test_df) - 1)

    # Plot data
    fig = px.line(test_df, x=test_df.index, y='casos', title='Série Prevista com Modelo AR')
    fig.add_scatter(x=test_df.index, y=forecast, mode='lines', name='Previsão')
    st.plotly_chart(fig, key=4)
    

elif model_option == 'ARIMA' or model_option == 'SARIMA':
    # Add a selectbox to select a new dataframe
    other_df_option = st.selectbox(
        'Selecione DataFrame da série que quer utiliar como covariável',
        options=['ZIKA', 'CHIK', 'AIDS']
    )

    if other_df_option == 'ZIKA':
        other_df = df_zika
    elif other_df_option == 'CHIK':
        other_df = df_chik
    elif other_df_option == 'AIDS':
        other_df = df_aids

    # Add a selectbox to filter by "sexo"
    other_sexo_option = st.selectbox(
        'Selecione o Gênero',
        options=[-1, 0, 1, 2],
        format_func=lambda x: 'Todos' if x == -1 else 'Não Identificado' if x == 0 else 'Masculino' if x == 1 else 'Feminino',
        key=1
    )

    # Add a selectbox to filter by "raca"
    other_raca_option = st.selectbox(
        'Selecione a Raça',
        options=[-1, 0, 1, 2, 3, 4, 5],
        format_func=lambda x: 'Todos' if x == -1 else 'Não Identificado' if x == 0 else 'Branca' if x == 1 else 'Preta' if x == 2 else 'Amarela' if x == 3 else 'Parda' if x == 4 else 'Indígena',
        key=2
    )

    # Add a slider to select age
    other_idade_option = st.slider(
        'Selecione a Idade',
        min_value=0,
        max_value=150,
        value=(0, 150),
        key=3
    )

    # Filter selected temporal series to model
    other_filtered_df = filter_df(other_df, start_date, end_date, other_sexo_option, other_raca_option, other_idade_option)

    other_train_size = int(len(other_filtered_df) * 0.8)
    other_train_df = other_filtered_df.iloc[:other_train_size]
    other_test_df = other_filtered_df.iloc[other_train_size:]

    if model_option == 'ARIMA':
        # Fit ARIMA model
        from statsmodels.tsa.arima.model import ARIMA

        model = ARIMA(train_df, other_train_df)
        model_fit = model.fit()

        # Forecast
        forecast = model_fit.forecast(steps=test_size, exog=other_test_df)

        # Plot data
        fig = px.line(test_df, x=test_df.index, y='casos', title='Série Prevista com Modelo ARIMA')
        fig.add_scatter(x=forecast.index, y=forecast, mode='lines', name='Previsão')
        st.plotly_chart(fig, key=4)

    elif model_option == 'SARIMA':
        # Fit SARIMA model
        from statsmodels.tsa.statespace.sarimax import SARIMAX

        model = SARIMAX(train_df, other_train_df)
        model_fit = model.fit()

        # Forecast
        forecast = model_fit.forecast(steps=test_size, exog=other_test_df)

        # Plot data
        fig = px.line(test_df, x=test_df.index, y='casos', title='Série Prevista com Modelo SARIMA')
        fig.add_scatter(x=forecast.index, y=forecast, mode='lines', name='Previsão')
        st.plotly_chart(fig, key=4)