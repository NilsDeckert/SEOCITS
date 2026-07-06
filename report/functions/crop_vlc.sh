#!/bin/bash

# This script takes VLC snapshots of the benchmark recordings and crops
# them to a uniform size. This is used to generate images for the presentation.

for img in vlcsnap*.png; do
    magick "$img" -crop 900x1100+500+300 "cropped_$img"
done
