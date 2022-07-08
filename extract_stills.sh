#!/bin/bash
dirs=(basement childsroom diningroom frontporch gallery kitchen livingroom studio)

for file in input-videos/*/*.avi; do
    destination="output${file:12:${#file}-17}";
    mkdir -p "$destination";
    ffmpeg -i "$file" -r 1 "$destination/image-%d.jpeg";
done