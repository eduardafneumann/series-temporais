from pysus.ftp.databases.sinan import SINAN
import os

if not os.path.exists('raw_data'):
    os.mkdir('raw_data')

if not os.path.exists('raw_data/dengue'):
    os.mkdir('raw_data/dengue')

sinan = SINAN().load()
files = sinan.get_files(dis_code=["DENG"])

for year_file in files:
    parquet = year_file.download()
    year_string = sinan.describe(year_file)['year']
    if(int(year_string) == 2002):
        df = parquet.to_dataframe()
        df.to_csv(f'raw_data/dengue/dengue_{year_string}.csv')
    
