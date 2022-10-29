import ffmpeg

# filename ="video.mov"
filename ="input-videos/livingroom/livingroom_motion_2017-08-13_10.26.55_5.mp4"

metadata = ffmpeg.probe(filename)
video_stream = next((stream for stream in metadata['streams'] if stream['codec_type'] == 'video'), None)

fps = metadata['streams'][0]['avg_frame_rate'].split('/')[0]
duration = metadata['streams'][0]['duration']

width = int(video_stream['width'])
height = int(video_stream['height'])

print(f'Width: {width}, Height: {height}, FPS: {fps}, Duration: {duration}')