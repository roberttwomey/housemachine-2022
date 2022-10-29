import ffmpeg
import os

def load_metadata(filename, prepostroll=10.0):
    metadata = ffmpeg.probe(filename)
    video_stream = next((stream for stream in metadata['streams'] if stream['codec_type'] == 'video'), None)

    fps = float(metadata['streams'][0]['avg_frame_rate'].split('/')[0])/1000.0
    duration = float(metadata['streams'][0]['duration'])

    width = int(video_stream['width'])
    height = int(video_stream['height'])

    print(f'Width: {width}, Height: {height}, FPS: {fps} fps, Duration: {duration} sec')
    print(fps)

    # calculating frame intervals
    # from here: https://api.video/blog/tutorials/extract-a-set-of-frames-from-a-video-with-ffmpeg-and-python
    action_duration = duration-prepostroll # prepostroll is length of pre and post in motion trigger
    print(action_duration)
    
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

    print(intervals)
    return intervals

def extract_frames(filename, intervals, height, outpath):
    
    path, file = os.path.split(filename)
    workfolder = path.split("/")[-1]
    filebase = os.path.splitext(file)[0]

    i=0
    for time in intervals:
        outfilename = "{0}_{1:02d}.jpg".format(filebase, i)
        outfile = os.path.join(outpath, outfilename)
        print(i, intervals, filename, outfile)

        (
            ffmpeg
            .input(filename, ss=time)
            .filter('scale', height, height) # width, -1)
            .output(outfile, vframes=1)
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
    print(files[:10])
    print(counts)

    for filename in files:
        duration, action_duration, width, height = load_metadata(filename)
        
        intervals = create_intervals(filename, duration, action_duration)

        extract_frames(filename, intervals, height, outpath="output/")
        # print(filename, duration)


if __name__ == "__main__":
    main()
