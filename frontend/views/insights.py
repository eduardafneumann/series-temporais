import streamlit as st
import plotly.express as px
import pandas as pd

# Load the Zika dataset
zika_df = pd.read_parquet('./data/ZIKA.parquet')
zika_df = zika_df.resample('D').count()
zika_df = zika_df[['sexo']].rename(columns={'sexo': 'casos'})

# Create a new column for the year of the date
zika_df['year'] = zika_df.index.year
zika_df['day_month'] = zika_df.index.strftime('%d-%m')

# Create a seasonal plot
fig = px.line(zika_df, x='day_month', y='casos', color='year', title='Seasonal Plot for Zika Data in Brazil')


# Display the plot in Streamlit
st.plotly_chart(fig)