import matplotlib.pyplot as plt
import pandas as pd

buoys = ['guam', 'gbma', 'smca', 'hilo', 'sjpr']

plt.figure(figsize=(10, 5))
for buoy in buoys:
    df = pd.read_csv(f"data/seastate_clusters/{buoy}.csv")
    plt.scatter(df['center_Tp'], df['center_Hs'], label=buoy)
plt.grid()
plt.xlabel('Wave Period (s)')
plt.ylabel('Wave Height (m)')
plt.legend()
plt.savefig("data/seastate_clusters/all_buoys.pdf")
plt.close()