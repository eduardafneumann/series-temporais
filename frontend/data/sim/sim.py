import pandas as pd

df = pd.read_csv('sim.csv')
df['ANO'] = df.apply(lambda row: str(row.DTOBITO)[-4:], axis = 1)
new_df = pd.DataFrame(data=df.value_counts(subset=['ANO']))
new_df.columns = ['OBITOS']
new_df.sort_index(inplace=True)
new_df.to_csv('sim_serie_anual.csv')