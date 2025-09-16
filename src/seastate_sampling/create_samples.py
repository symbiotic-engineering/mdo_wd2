import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_Hm0_Te_from_ndbc(file_path):
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

    # Set datetime as index and extract Hm0 and Te
    Hm0 = df.set_index('datetime')['WVHT']
    Te = df.set_index('datetime')['DPD']

    return Hm0, Te

buoys = ['guam', 'gbma', 'smca', 'hilo', 'sjpr']
years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']

wave_data = {buoy:{} for buoy in buoys}

for buoy in buoys:
    hm0_list = []
    te_list = []
    for year in years:
        file_path = f'data/NDBC_data/{buoy}_{year}.txt'
        try:
            Hm0, Te = get_Hm0_Te_from_ndbc(file_path)
            hm0_list.append(Hm0)
            te_list.append(Te)
            print(f'Loaded {len(Hm0)} records for {buoy} in {year}')
        except FileNotFoundError:
            print(f'File not found: {file_path}')
        except Exception as e:
            print(f'Error processing {file_path}: {e}')

    # Filter out Hm0 > 20 and Te > 40
    Hm0 = pd.concat(hm0_list)
    Te = pd.concat(te_list)
    mask = (Hm0 <= 20) & (Te <= 40)
    Hm0 = Hm0[mask]
    Te = Te[mask]

    # Concatenate and convert to NumPy arrays
    wave_data[buoy]['Hm0'] = Hm0.values
    wave_data[buoy]['Te'] = Te.values
    

# Quick check
for buoy in buoys:
    if 'Hm0' in wave_data[buoy]:
        print(buoy, wave_data[buoy]['Hm0'].shape, wave_data[buoy]['Te'].shape)

# Plots of data
plt.figure(figsize=(10, 5))
plt.scatter(wave_data['guam']['Te'], wave_data['guam']['Hm0'], alpha=0.5)
plt.xlabel('Peak Period (Te)')
plt.ylabel('Significant Wave Height (Hm0)')
plt.title('Wave Data for Guam Buoy')
plt.grid()
plt.savefig('guam_wave_data.png')
plt.figure(figsize=(10, 5))
plt.scatter(wave_data['gbma']['Te'], wave_data['gbma']['Hm0'], alpha=0.5)
plt.xlabel('Peak Period (Te)')
plt.ylabel('Significant Wave Height (Hm0)')
plt.title('Wave Data for GBMA Buoy')
plt.grid()
plt.savefig('gbma_wave_data.png')
plt.figure(figsize=(10, 5))
plt.scatter(wave_data['smca']['Te'], wave_data['smca']['Hm0'], alpha=0.5)
plt.xlabel('Peak Period (Te)')
plt.ylabel('Significant Wave Height (Hm0)')
plt.title('Wave Data for SMCA Buoy')
plt.grid()
plt.savefig('smca_wave_data.png')
plt.figure(figsize=(10, 5))
plt.scatter(wave_data['hilo']['Te'], wave_data['hilo']['Hm0'], alpha=0.5)
plt.xlabel('Peak Period (Te)')
plt.ylabel('Significant Wave Height (Hm0)')
plt.title('Wave Data for Hilo Buoy')
plt.grid()
plt.savefig('hilo_wave_data.png')
plt.figure(figsize=(10, 5))
plt.scatter(wave_data['sjpr']['Te'], wave_data['sjpr']['Hm0'], alpha=0.5)
plt.xlabel('Peak Period (Te)')
plt.ylabel('Significant Wave Height (Hm0)')
plt.title('Wave Data for SJPR Buoy')
plt.grid()
plt.savefig('sjpr_wave_data.png')
