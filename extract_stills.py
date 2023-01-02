import ffmpeg
import os
from tqdm import tqdm
import json

def load_metadata(filename, prepostroll=10.0):
    metadata = ffmpeg.probe(filename)
    video_stream = next((stream for stream in metadata['streams'] if stream['codec_type'] == 'video'), None)

    fps = float(metadata['streams'][0]['avg_frame_rate'].split('/')[0])/1000.0
    duration = float(metadata['streams'][0]['duration'])

    width = int(video_stream['width'])
    height = int(video_stream['height'])

    # calculating frame intervals
    # from here: https://api.video/blog/tutorials/extract-a-set-of-frames-from-a-video-with-ffmpeg-and-python
    action_duration = duration-prepostroll # prepostroll is length of pre and post in motion trigger
    
    #print(f'Width: {width}, Height: {height}, FPS: {fps} fps, Duration: {duration} sec, action_duration: {action_duration}')
    
    return (duration, action_duration, width, height)

def create_intervals(filename, duration, action_duration):
    # extract before (pre-motion)
    intervals = [2.5]

    # sample motion section (1fps or similar)
    # if action_duration >= 1.0:
    #     parts = 3
    # else: 
    #     parts = 1

    parts = int(action_duration/10.0)+1
    middlepoints = [5.0+((i+1)*action_duration)/(parts+1) for i in range(parts)]
    intervals += middlepoints

    # extract after (post_motion)
    intervals+=[duration-2.5]

    # print(intervals)
    return intervals

def create_intervals2(filename, duration, action_duration):
    fps = 15.0
    f_len = 1.0/fps
    starttime = 5.0

    samples_per_second = 5.0
    sample_interval = (1.0/samples_per_second)
    
    intervals = []
    if duration > 11.0:    
        # extract only frames from action segment
        t = starttime
        # while t < starttime+action_duration:
        while t < duration:
            intervals.append(t)
            t+=sample_interval
    else: 
        intervals = [5.0]

    return intervals
    

def extract_frames(filename, intervals, height, outpath):
    
    path, file = os.path.split(filename)
    workfolder = path.split("/")[-1]
    filebase = os.path.splitext(file)[0]

    i=0
    for time in intervals:
        outfilename = "{0}_{1:02d}.jpg".format(filebase, i)
        outfile = os.path.join(outpath, outfilename)
        # print(i, intervals, filename, outfile)

        (
            ffmpeg
            .input(filename, ss=time)
            .filter('scale', height, height) # width, -1)
            .output(outfile, vframes=1, loglevel="quiet")
            .overwrite_output()
            .run()
        )
        i += 1

def walk_files(path):
    data_dirs = [ 
        "basement", 
        "childsroom", 
        "diningroom", 
        "frontporch",
        "kitchen",
        "livingroom",
        "studio"
        ] 

    vidfiles = []
    counts = {}
    for dirpath, subdirs, files in os.walk(path):
        for x in files:
            if x.endswith(".mp4"):
                lastsubfolder = dirpath.split("/")[-1]
                if lastsubfolder in data_dirs:
                    if lastsubfolder in counts:
                        counts[lastsubfolder]+=1
                    else:
                        counts[lastsubfolder]=1
                    vidfiles.append(os.path.join(dirpath, x))

    return (vidfiles, counts)

def main():
    
    # filename ="video.mov"
    # filename ="input-videos/livingroom/livingroom_motion_2017-08-13_10.26.55_5.mp4"

    files, counts = walk_files("input-videos/")
    # print(files)
    print("counts for each room: ", counts)
    file_count = len(files)
    intervals = {}
    still_count = 0

    if not os.path.exists("intervals.json"):
        print("calculating intervals:")
        with tqdm(total=file_count) as pbar:  # Do tqdm this way
            for filename in files:
                duration, action_duration, width, height = load_metadata(filename, prepostroll=10.0) # action starts 
                
                # intervals = create_intervals(filename, duration, action_duration)
                intervals[filename] = create_intervals2(filename, duration, action_duration) # only action parts
                # print(filename, intervals)

                still_count += len(intervals[filename])
                pbar.update(1)  # Increment the progress bar

        print("writing out intervals to json file")
        with open("intervals.json", "w") as outfile:
            json.dump(intervals, outfile)
    else: 
        with open('intervals.json', 'r') as openfile:
            # Reading from json file
            intervals = json.load(openfile)
            still_count = sum(len(lst) for dct in intervals.values() for lst in intervals.values())

    print("extracting frames:")
    with tqdm(total=still_count) as pbar:  # Do tqdm this way
        for filename in files:
            extract_frames(filename, intervals[filename], height, outpath="output/")
            # print(filename, duration)

            pbar.update(len(intervals[filename]))  # Increment the progress bar


if __name__ == "__main__":
    main()
