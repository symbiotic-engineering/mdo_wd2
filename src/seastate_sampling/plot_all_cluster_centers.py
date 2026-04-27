import matplotlib.pyplot as plt
import pandas as pd

buoys = ['guam', 'gbma', 'smca', 'hilo', 'sjpr']
name = {"guam": "Guam", "gbma": "Georges Bank, MA", "smca": "Santa Monica Bay, CA", "hilo": "Hilo Bay, HI", "sjpr": "San Juan, PR"}

plt.figure(figsize=(10, 5))
for buoy in buoys:
    df = pd.read_csv(f"data/seastate_clusters_10/{buoy}.csv")
    plt.scatter(df['center_Tp'], df['center_Hs'], label=name[buoy],s=80)

df = pd.read_csv(f"data/seastate_clusters_10/clusterclusters.csv")
plt.scatter(df['center_Tp'], df['center_Hs'],marker='x',s=160, label="Final Clusters",color='black')
plt.grid()
plt.xlabel('Wave Period (s)')
plt.ylabel('Wave Height (m)')
plt.legend()
plt.savefig("data/seastate_clusters_10/all_buoys_clusterclusters.pdf")
plt.close()