import ffmpeg

# filename ="video.mov"
filename ="input-videos/livingroom/livingroom_motion_2017-08-13_10.26.55_5.mp4"

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
action_duration = duration-10.0
print(action_duration)

# extract before (pre-motion)
intervals = [2.5]

# sample motion section (1fps or similar)
if action_duration >= 1.0:
	parts = 3
else: 
	parts = 1

middlepoints = [5.0+i*(action_duration)/parts for i in range(parts)]
intervals += middlepoints

# extract after (post_motion)
intervals+=[duration-2.5]

print(intervals)


i=0
for item in intervals:
    (
        ffmpeg
        .input(filename, ss=item)
        .filter('scale', width, -1)
        .output('Image' + str(i) + '.jpg', vframes=1)
        .run()
    )
    i += 1