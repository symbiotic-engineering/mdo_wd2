import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_folder)
from src.seastate_sampling.kmeans_clustering import build_clusters
import csv
import mhkit.wave as wave

def get_Hm0_Te_from_ndbc(file_path):
    [raw_ndbc_data, meta] = wave.io.ndbc.read_file(file_path)
    ndbc_data = raw_ndbc_data.T
    Te = wave.resource.peak_period(ndbc_data)
    Hm0 = wave.resource.significant_wave_height(ndbc_data)
    return Hm0, Te

years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']


for year in years:
    ndbc_file = f'data/NDBC_data/gbma_{year}_spectral.txt'
    Hm0, Te = get_Hm0_Te_from_ndbc(ndbc_file)
    if year == years[0]:
        wave_data = {}
        wave_data['Hm0'] = Hm0.values
        wave_data['Te'] = Te.values
    else:
        wave_data['Hm0'] = np.concatenate((wave_data['Hm0'], Hm0.values))
        wave_data['Te'] = np.concatenate((wave_data['Te'], Te.values))
    

plt.figure(figsize=(10, 5))
plt.scatter(wave_data['Te'], wave_data['Hm0'], alpha=0.5)
plt.xlabel('Peak Period (Te)')
plt.ylabel('Significant Wave Height (Hm0)')
plt.title(f'Spectral Wave Data for Buoy')
plt.grid()
plt.savefig(f'spectral_wave_data.png')
plt.close()

k = 10
iterations = 50
X = np.vstack((wave_data['Te'], wave_data['Hm0'])).T
wave_data['clusters'],pred = build_clusters(X,k,iterations)

# write clusters to csv
os.makedirs('data/seastate_clusters', exist_ok=True)
csv_path = f'data/seastate_clusters/spectral.csv'
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['cluster_id', 'center_Te', 'center_Hm0', 'count'])
    for cluster_id, info in wave_data['clusters'].items():
        center_Te, center_Hm0 = info['center']
        count = len(info['points'])
        writer.writerow([cluster_id, center_Te, center_Hm0, count])

plt.figure(figsize=(10, 5))
plt.scatter(X[:,0],X[:,1],c = pred)
plt.xlabel('Peak Period (Te)')
plt.ylabel('Significant Wave Height (Hm0)')
plt.title(f'Spectral Wave Data Clustering for Buoy')
plt.grid()
for i in wave_data['clusters']:
    center = wave_data['clusters'][i]['center']
    plt.scatter(center[0],center[1],marker = '^',c = 'red')
plt.savefig(f'spectral_clusters.png')
plt.close()