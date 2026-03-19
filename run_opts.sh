#!/bin/bash

wave_heights=(1.1146362808579522)
peak_periods=(22.584459732902232)

for i in "${!wave_heights[@]}"; do
  wave_height="${wave_heights[$i]}"
  peak_period="${peak_periods[$i]}"
  python src/optrun.py --wave_height "$wave_height" --peak_period "$peak_period"
done