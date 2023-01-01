# housemachine-2022
Machine for Living In work for 2022-2023
- training StyleGAN3 on stills from housemachine
- generating motion trial drawings from json tracking data

--
# setup
to link old recordings files: 

`ln -s /Volumes/Work/Projects/housemachine/data/ceiling input-videos`

`mkdir output`

`./extract_stills.sh`

## Local (macos) data prep

cd /Volumes/Work/Projects/housemachine-2022
conda activate housemachine
python extract_stills.py

