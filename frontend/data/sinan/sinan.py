import pandas as pd

# df = pd.read_csv('chik.csv', encoding='latin-1')
# df['ANO'] = df.apply(lambda row: str(row.DT_NOTIFIC)[0:4], axis = 1)
# new_df = pd.DataFrame(data=df.value_counts(subset=['ANO']))
# new_df.columns = ['CASOS']
# new_df.sort_index(inplace=True)
# new_df.to_csv('chik_serie_anual.csv')

# df = pd.read_csv('zika.csv')
# df['ANO'] = df.apply(lambda row: str(row.DT_NOTIFIC)[0:4], axis = 1)
# new_df = pd.DataFrame(data=df.value_counts(subset=['ANO']))
# new_df.columns = ['CASOS']
# new_df.sort_index(inplace=True)
# new_df.to_csv('zika_serie_anual.csv')

# df = pd.read_csv('aids.csv')
# df = df.loc[df['DT_NOTIFIC'] != "********"]
# df['ANO'] = df.apply(lambda row: str(row.DT_NOTIFIC)[0:4], axis = 1)
# new_df = pd.DataFrame(data=df.value_counts(subset=['ANO']))
# new_df.columns = ['CASOS']
# new_df.sort_index(inplace=True)
# new_df.to_csv('aids_serie_anual.csv')

# df = pd.read_csv('deng2.csv')
# df['ANO'] = df.apply(lambda row: str(row.DT_NOTIFIC)[0:4], axis = 1)
# new_df = pd.DataFrame(data=df.value_counts(subset=['ANO']))
# new_df.columns = ['CASOS']
# new_df.sort_index(inplace=True)
# new_df.to_csv('dengue2_serie_anual.csv')

# df = pd.read_csv('deng1.csv')
# df['ANO'] = df.apply(lambda row: str(row.DT_NOTIFIC)[0:4], axis = 1)
# new_df = pd.DataFrame(data=df.value_counts(subset=['ANO']))
# new_df.columns = ['CASOS']
# new_df.sort_index(inplace=True)
# new_df.to_csv('dengue1_serie_anual.csv')

# df1 = pd.read_csv('dengue1_serie_anual.csv')
# df2 = pd.read_csv('dengue2_serie_anual.csv')
# df = pd.concat([df1, df2], axis=0)
# df.set_index('ANO', inplace=True)
# df.to_csv('dengue_serie_anual.csv')