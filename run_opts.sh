#!/bin/bash

wave_heights=(1.4757467428690545)
peak_periods=(10.234793700202095)

for i in "${!wave_heights[@]}"; do
  wave_height="${wave_heights[$i]}"
  peak_period="${peak_periods[$i]}"
  python src/optrun.py --wave_height "$wave_height" --peak_period "$peak_period"
done