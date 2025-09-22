from mhkit import wave

lat_lon = [19.74, -155.07]
region = wave.io.hindcast.hindcast.region_selection(lat_lon)
print(region)

year = "2018"  # only one year can be passed at a time as a string
lat_lon = (19.779, -154.97)
dir_spectra, meta = wave.io.hindcast.hindcast.request_wpto_directional_spectrum(
    lat_lon, year
)

print(dir_spectra)