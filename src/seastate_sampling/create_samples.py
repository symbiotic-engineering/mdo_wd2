import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_folder)
from src.seastate_sampling.kmeans_clustering import build_clusters
import csv

def get_Hs_Tp_from_ndbc(file_path):
    """
    Reads an NDBC-style buoy file and returns significant wave height (WVHT)
    and peak period (DPD) as pandas Series indexed by datetime.
    """
    # Read file, skip first 2 comment lines
    df = pd.read_csv(
        file_path,
        sep=r'\s+',
        skiprows=2,
        header=None
    )

    # Assign proper column names
    df.columns = ['YY','MM','DD','hh','mm','WDIR','WSPD','GST',
                  'WVHT','DPD','APD','MWD','PRES','ATMP','WTMP',
                  'DEWP','VIS','TIDE']

    # Ensure numeric types
    for col in ['YY','MM','DD','hh','mm','WVHT','DPD']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Rename columns to what pd.to_datetime expects
    df = df.rename(columns={'YY':'year', 'MM':'month', 'DD':'day',
                            'hh':'hour', 'mm':'minute'})

    # Create datetime column
    df['datetime'] = pd.to_datetime(df[['year','month','day','hour','minute']])

    # Set datetime as index and extract Hs and Tp
    Hs = df.set_index('datetime')['WVHT']
    Tp = df.set_index('datetime')['DPD']

    return Hs, Tp

buoys = ['guam', 'gbma', 'smca', 'hilo', 'sjpr']
years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

wave_data = {buoy:{} for buoy in buoys}

for buoy in buoys:
    hs_list = []
    tp_list = []
    for year in years:
        file_path = f'data/NDBC_data/{buoy}_{year}.txt'
        try:
            Hs, Tp = get_Hs_Tp_from_ndbc(file_path)
            hs_list.append(Hs)
            tp_list.append(Tp)
            print(f'Loaded {len(Hs)} records for {buoy} in {year}')
        except FileNotFoundError:
            print(f'File not found: {file_path}')
        except Exception as e:
            print(f'Error processing {file_path}: {e}')

    # Filter out Hs > 20 and Tp > 40
    Hs = pd.concat(hs_list)
    Tp = pd.concat(tp_list)
    mask = (Hs <= 20) & (Tp <= 40)
    Hs = Hs[mask]
    Tp = Tp[mask]

    # Concatenate and convert to NumPy arrays
    wave_data[buoy]['Hs'] = Hs.values
    wave_data[buoy]['Tp'] = Tp.values

# Quick check
for buoy in buoys:
    if 'Hs' in wave_data[buoy]:
        print(buoy, wave_data[buoy]['Hs'].shape, wave_data[buoy]['Tp'].shape)

# Plots of data
'''def plot_wave_data(wave_data, buoy):
    plt.figure(figsize=(10, 5))
    plt.scatter(wave_data[buoy]['Tp'], wave_data[buoy]['Hs'], alpha=0.5)
    plt.xlabel('Peak Period (Tp)')
    plt.ylabel('Significant Wave Height (Hs)')
    plt.title(f'Wave Data for {buoy.upper()} Buoy')
    plt.grid()
    plt.savefig(f'{buoy}_wave_data.png')
    plt.close()
for buoy in buoys:
    plot_wave_data(wave_data, buoy)'''
   
k = 10
iterations = 100
for buoy in buoys:
    print(f'Clustering for {buoy} buoy...')
    X = np.vstack((wave_data[buoy]['Tp'], wave_data[buoy]['Hs'])).T
    wave_data[buoy]['clusters'],pred = build_clusters(X,k,iterations)
    print(f'Clustering complete for {buoy} buoy')

    # write clusters to csv
    os.makedirs('data/seastate_clusters', exist_ok=True)
    csv_path = f'data/seastate_clusters/{buoy}.csv'
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['cluster_id', 'center_Tp', 'center_Hs', 'count'])
        for cluster_id, info in wave_data[buoy]['clusters'].items():
            center_Tp, center_Hs = info['center']
            count = len(info['points'])
            writer.writerow([cluster_id, center_Tp, center_Hs, count])

    plt.figure(figsize=(10, 5))
    plt.scatter(X[:,0],X[:,1],c = pred)
    plt.xlabel('Peak Period (Tp)')
    plt.ylabel('Significant Wave Height (Hs)')
    plt.title(f'Wave Data Clustering for {buoy.upper()} Buoy')
    plt.grid()
    for i in wave_data[buoy]['clusters']:
        center = wave_data[buoy]['clusters'][i]['center']
        plt.scatter(center[0],center[1],marker = '^',c = 'red')
    plt.savefig(f'data/seastate_clusters/{buoy}_clusters.pdf')
    plt.close()

