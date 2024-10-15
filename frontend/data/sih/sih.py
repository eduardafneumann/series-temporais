import pandas as pd

df = pd.read_csv('sih.csv')
df['ANO'] = df.apply(lambda row: str(row.DT_INTER)[0:4], axis = 1))
new_df = pd.DataFrame(data=df.value_counts(subset=['ANO']))
new_df.columns = ['INTER']
new_df.sort_index(inplace=True)
new_df.to_csv('sih_serie_anual.csv')