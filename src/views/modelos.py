import pandas as pd
import streamlit as st
import plotly.express as px
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import acf, pacf
from scipy.stats import shapiro

arima_aids_coff = (2, 1, 2)
arima_zika_coff = (5, 1, 4)
arima_chik_coff = (5, 1, 3)

st.write(""" 
         # DataSUS - Sinan - Previsão das Séries   
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

df_option = st.selectbox(
    'Selecione a série',
    options=['ZIKA', 'CHIK', 'AIDS']
)

model_option = st.selectbox(
    'Selecione o modelo',
    options=['ARIMA', 'SARIMA', 'Autoregressivo']
)

if df_option == "ZIKA":
    df = df_zika
    arima_coff = arima_zika_coff
elif df_option == "CHIK":
    df = df_chik
    arima_coff = arima_chik_coff
elif df_option == "AIDS":
    df = df_aids
    arima_coff = arima_aids_coff

if model_option == "ARIMA":

    st.text(f"Os parâmetros do modelo ARIMA sugeridos são {arima_coff}. Se desejar, mude os parâmetros abaixo.")

    c1, c2, c3 = st.columns(3)

    with c1:
        p = st.number_input(
            label="Parâmetro p:",
            min_value=0,
            max_value=10,
            value=arima_coff[0],
            step=1
        )

    with c2:
        d = st.number_input(
            label="Parâmetro d:",
            min_value=0,
            max_value=10,
            value=arima_coff[1],
            step=1
        )

    with c3:
        q = st.number_input(
            label="Parâmetro q:",
            min_value=0,
            max_value=10,
            value=arima_coff[2],
            step=1
        )






    # Group by DT_NOTIFIC and count the number of cases
    df_cases_count = df.groupby('data').size().reset_index(name='Number of Cases')
    train_data = df_cases_count[df_cases_count['data'].dt.year < 2023]
    test_data = df_cases_count[df_cases_count['data'].dt.year == 2023]

    # model = auto_arima(train_data['Number of Cases'], seasonal=False)
    # print(model.summary())
    
    model_cases = ARIMA(train_data['Number of Cases'], order=(p, d, q))  # Order (p, d, q)
    model_cases_fit = model_cases.fit()
    forecast_steps = len(test_data)
    forecast_cases = model_cases_fit.get_forecast(steps=forecast_steps)
    pred_mean_cases = forecast_cases.predicted_mean

    residuals = test_data['Number of Cases'] - pred_mean_cases
    std_residuals = residuals / np.std(residuals, ddof=1)  # Studentized residuals
    test_data['Studentized Residuals'] = std_residuals


    



    # PLOTAR PREVISÃO E VALORES REAIS

    df_plot = pd.DataFrame({'Casos observados' : test_data['Number of Cases'], 
                            "Casos previstos" : pred_mean_cases,
                            "Tempo" : test_data['data']})
    fig = px.line(df_plot, 
        title = "Previsão",
        x="Tempo",
        y=["Casos observados", "Casos previstos"]
    )
    fig['data'][1]['line']['color']='red'
    fig.update_layout(legend_title_text="Legenda")
    st.plotly_chart(fig)





    # PLOTAR RESIDUOS STUDENTIZADOS

    fig = px.scatter(
        test_data, 
        x='data', 
        y='Studentized Residuals', 
        title='Resíduos studentizados',
        labels={'data': 'Tempo', 'Studentized Residuals': 'Resíduos Studentizados'},
        opacity=0.6
    )
    fig.add_hline(y=0, line_color="red", line_dash="solid", name="Zero")
    fig.add_hline(y=2, line_color="red", line_dash="dash", name="Limite Superior")
    fig.add_hline(y=-2, line_color="red", line_dash="dash", name="Limite Inferior")
    fig.update_traces(marker=dict(color='blue'))
    fig.update_layout(showlegend=True)
    fig.update_layout(legend_title_text="Legenda")
    st.plotly_chart(fig)

    qtd_residuos_outliers = 0
    for y in test_data['Studentized Residuals']:
        if y > 2 or y < -2:
            qtd_residuos_outliers += 1
    porcentagem_residuos_outliers = round(100 * qtd_residuos_outliers/len(test_data['Studentized Residuals']), 4)
    st.text(f'{porcentagem_residuos_outliers}% dos resíduos studentizados ficam a mais de dois desvios padrões da média.')







    # PLOTAR DISTRIBUIÇÃO DOS RESIDUOS
    
    fig = px.histogram(
        std_residuals, 
        nbins=20, 
        histnorm='probability density',  # Normaliza para densidade
        opacity=0.6, 
        labels={'value': 'Resíduos Padronizados'}, 
        title='Distribuição dos resíduos'
    )
    fig.update_yaxes(title_text="Densidade")
    fig.data[0].name = "Histograma"
    fig.data[0].showlegend = True
    # Adicionar a curva de densidade estimada
    x_vals = np.linspace(std_residuals.min(), std_residuals.max(), 100)
    kde = gaussian_kde(std_residuals)
    y_vals = kde.evaluate(x_vals)
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines',
        name='Densidade',
        line=dict(color='red'),
    ))
    fig.update_layout(legend_title_text="Legenda")
    st.plotly_chart(fig)





    # TESTE DE NORMALIDADE DOS RESÍDUOS

    shapiro_stat, shapiro_p = shapiro(residuals)
    st.text(f'O valor do estatístico do teste de Shapiro-Wilk, que verifica se os dados seguem uma distribuição normal, sobre os resíduos é aproximadamente {round(shapiro_stat, 6)}, com p valor aproximadamente {round(shapiro_p, 6)}.')
    if shapiro_p < 0.05:
        st.text(f'O p valor ser menor que 5% indica que os resíduos não têm distribuíção normal.')
    else:
        st.text(f'O p valor ser maior que 5% indica que os resíduos têm distribuíção normal.')






    # PLOTAR ACF E PACF

    c1, c2 = st.columns(2)

    with c1:
        fig = plot_acf(std_residuals, lags=20, title='Função de autocorrelação dos resíduos')
        st.pyplot(fig)

    with c2:
        fig = plot_pacf(std_residuals, lags=20, title='Função de autocorrelação parcial dos resíduos')
        st.pyplot(fig)






