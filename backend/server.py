from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load data
def load_data():
    df_zika = pd.read_parquet('frontend/data/ZIKA.parquet')
    df_chik = pd.read_parquet('frontend/data/CHIK.parquet')
    df_deng = None  # Assuming DENG data is not available
    df_aids = pd.read_parquet('frontend/data/AIDS.parquet')
    return df_zika, df_chik, df_deng, df_aids

# Function to filter dataframe by time
def filter_df_time(df, start_date, end_date):
    return df[(df.index.date >= start_date) & (df.index.date <= end_date)]

# Function to filter dataframe
def filter_df(df, start_date, end_date, sexo_option, raca_option, idade_option, disease, frequency):
    df = filter_df_time(df, start_date, end_date)
    if sexo_option != -1:
        df = df[df['sexo'] == sexo_option]
    if raca_option != -1:
        df = df[df['raca'] == raca_option]
    df = df[(df['idade'] >= idade_option[0]) & (df['idade'] <= idade_option[1])]
    df = df.resample(frequency).count()
    df = df[['sexo']].rename(columns={'sexo': 'casos'})
    df['doenca'] = disease
    return df

# Endpoint to get combined dataframe
@app.route('/get_combined_df', methods=['GET'])
def get_combined_df():
    dfs_option = request.headers.get('dfs_option').split(',')
    start_date = pd.to_datetime(request.headers.get('start_date')).date()
    end_date = pd.to_datetime(request.headers.get('end_date')).date()
    sexo_option = int(request.headers.get('sexo_option'))
    raca_option = int(request.headers.get('raca_option'))
    idade_option = list(map(int, request.headers.get('idade_option').split(',')))
    frequency_option = request.headers.get('frequency_option')

    df_zika, df_chik, df_deng, df_aids = load_data()

    filtered_dfs = []
    if 'ZIKA' in dfs_option:
        filtered_dfs.append(filter_df(df_zika, start_date, end_date, sexo_option, raca_option, idade_option, 'ZIKA', frequency_option))
    if 'CHIK' in dfs_option:
        filtered_dfs.append(filter_df(df_chik, start_date, end_date, sexo_option, raca_option, idade_option, 'CHIK', frequency_option))
    if 'DENG' in dfs_option:
        filtered_dfs.append(filter_df(df_deng, start_date, end_date, sexo_option, raca_option, idade_option, 'DENG', frequency_option))
    if 'AIDS' in dfs_option:
        filtered_dfs.append(filter_df(df_aids, start_date, end_date, sexo_option, raca_option, idade_option, 'AIDS', frequency_option))

    combined_df = pd.concat(filtered_dfs)
    return combined_df.to_json(orient='split')

# Endpoint to get dfs to plot (sazonal)
@app.route('/get_dfs_to_plot_sazonal', methods=['GET'])
def get_dfs_to_plot_sazonal():
    print(request.headers)
    dfs_option = request.headers.get('dfs-option').split(',')
    start_date = pd.to_datetime(request.headers.get('start-date')).date()
    end_date = pd.to_datetime(request.headers.get('end-date')).date()

    df_zika, df_chik, df_deng, df_aids = load_data()

    df_dict = {
        'ZIKA': df_zika,
        'CHIK': df_chik,
        'AIDS': df_aids,
        'DENG': df_deng
    }

    dfs_to_plot = []

    for disease in dfs_option:
        df = df_dict[disease]
        df = df[(df.index.date >= start_date) & (df.index.date <= end_date)]
        df = df.resample('ME').count()
        df = df[['sexo']].rename(columns={'sexo': 'casos'})
        df['ano'] = df.index.year
        df['mes'] = df.index.month_name()
        dfs_to_plot.append((df, disease))

    result = {disease: df.to_json(orient='split') for df, disease in dfs_to_plot}
    return jsonify(result)

# Endpoint to get dfs to plot (categoria)
@app.route('/get_dfs_to_plot_categoria', methods=['GET'])
def get_dfs_to_plot_categoria():
    dfs_option = request.headers.get('dfs_option').split(',')
    column_option = request.headers.get('column_option')
    values_options = request.headers.get('values_options').split(',')

    df_zika, df_chik, df_deng, df_aids = load_data()

    def process_df(df, column_option, values_transformed):
        df = df[(df.index.date >= start_date) & (df.index.date <= end_date)]
        df = df[[column_option]]
        df[column_option] = df[column_option].apply(lambda x: x if x in values_transformed else None)
        df = pd.get_dummies(df, columns=[column_option], prefix="", prefix_sep="")
        df.columns = df.columns.astype(float).astype(int)
        df = df.resample('ME').sum()
        df = df.rename(columns=get_inverted_dict(column_option))
        df = df.reset_index()
        df = pd.melt(df, id_vars=['data'], var_name='categoria', value_name='casos')
        df = df.set_index('data')
        return df

    def get_values_transformed(column, values):
        if column == 'sexo':
            return [sex_codes[value] for value in values]
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

    values_transformed = get_values_transformed(column_option, values_options)

    df_dict = {
        'ZIKA': df_zika,
        'CHIK': df_chik,
        'AIDS': df_aids,
        'DENG': df_deng
    }

    dfs_to_plot = []

    for disease in dfs_option:
        df = df_dict[disease]
        df = process_df(df, column_option, values_transformed)
        dfs_to_plot.append((df, disease))

    result = {disease: df.to_json(orient='split') for df, disease in dfs_to_plot}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)