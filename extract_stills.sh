#!/bin/bash
#dirs=(basement childsroom diningroom frontporch gallery kitchen livingroom studio)
for file in input-videos/*/*.mp4; do
    destination="output${file:12:${#file}-17}";
    # echo "$destination | cut -d'/' -f 3";
    filename=$(echo $destination | cut -d'/' -f 3);
    # echo $filename
    # duration=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file")
    # remainder=$(echo "$duration"-10 | bc)
    # echo $remainder
    
    ffmpeg -ss 0:10 -hide_banner -loglevel error -i "$file" -q:v 1 -r 3 "output/$filename-%d.jpg";
    # ffmpeg -ss 0:10 -r 1 -hide_banner -loglevel error -i "$file" -frames:v 1 -q:v 1 "output/$filename-%d.jpg";
    # ffmpeg -ss 0:11 -hide_banner -loglevel error -i "$file" -frames:v 1 -q:v 1 "$destination-%d.jpg";

    # ORIGINAL with nested subdirectories
    # mkdir -p "$destination";
    # ffmpeg -skip_frame nokey -i "$file"-vsync 0 -r 3 "$destination/image-%d.jpg";

done

# #!/bin/bash
# #dirs=(basement childsroom diningroom frontporch gallery kitchen livingroom studio)
# for file in input-videos/*/*.mp4; do
#     destination="output${file:12:${#file}-17}";
#     mkdir -p "$destination";
#     ffmpeg -i "$file" -r 1 "$destination/image-%d.jpg";
# done

# getting time from: https://superuser.com/a/945604
# ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$file" -sexagesimal
