import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('data/sim/sim_serie_anual.csv')

st.plotly_chart(px.line(df, x='ANO', y='OBITOS', title='Óbtios por ano'))