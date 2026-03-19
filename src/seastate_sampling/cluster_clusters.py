import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_folder)
from src.seastate_sampling.kmeans_clustering import build_clusters
import csv

def read_centers_from_csv(csv_path):
    """
    Read a CSV file containing at least the columns 'center_Tp' and 'center_Hs'
    (optionally 'cluster_id' to control ordering) and return two 1D numpy arrays:
    (center_Tp_array, center_Hs_array).
    """
    df = pd.read_csv(csv_path)
    required = {"center_Tp", "center_Hs"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {', '.join(required)}")
    if "cluster_id" in df.columns:
        df = df.sort_values("cluster_id")
    return df["center_Tp"].to_numpy(dtype=float), df["center_Hs"].to_numpy(dtype=float)

buoys = ['guam', 'gbma', 'smca', 'hilo', 'sjpr']
Tp = np.array([])
Hs = np.array([])
for buoy in buoys:
    csv_path = f'data/seastate_clusters_10/{buoy}.csv'
    center_Tp, center_Hs = read_centers_from_csv(csv_path)
    Tp = np.concatenate((Tp, center_Tp))
    Hs = np.concatenate((Hs, center_Hs))

k = 20
iterations = 100
X = np.vstack((Tp, Hs)).T
clusters,pred=build_clusters(X,k,iterations)

# write clusters to csv
csv_path = f'data/seastate_clusters_10/clusterclusters.csv'
with open(csv_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['cluster_id', 'center_Tp', 'center_Hs', 'count'])
    for cluster_id, info in clusters.items():
        center_Tp, center_Hs = info['center']
        count = len(info['points'])
        writer.writerow([cluster_id, center_Tp, center_Hs, count])

plt.figure(figsize=(10, 5))
plt.scatter(X[:,0],X[:,1],c = pred)
plt.xlabel('Peak Period (Tp)')
plt.ylabel('Significant Wave Height (Hs)')
plt.title(f'Wave Data Clustering for Clusters')
plt.grid()
for i in clusters:
    center = clusters[i]['center']
    plt.scatter(center[0],center[1],marker = '^',c = 'red')
plt.savefig(f'data/seastate_clusters/clusters_clusters.pdf')
plt.close()
