import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('data/sih/sih_serie_anual.csv')

st.plotly_chart(px.line(df, x='ANO', y='INTER', title='Internações por ano'))