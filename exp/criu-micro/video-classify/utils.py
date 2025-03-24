from moviepy.video.io.VideoFileClip import VideoFileClip

import random
import logging



# serilize VideoFileClip
def serialize_video_file_clip(filename: str, vfc: VideoFileClip):
    assert isinstance(vfc, VideoFileClip)
    # filename = tmp_folder + 'tmp' + str(random.randint(0, 10 ** 10)) + '.mp4'
    # It seems ffmpeg is buggy when there are concurrent requests with the same file name.
    # We add a random number to the file name to avoid this.
    vfc.write_videofile(filename, logger=None)

# deserialize VideoFileClip
def deserialize_video_file_clip(tmp_folder: str, bits: bytes):
    assert isinstance(bits, bytes)
    filename = tmp_folder + 'tmp' + str(random.randint(0, 10 ** 10)) + '.mp4'
    with open(filename, 'wb') as f:
        f.write(bits)
    return VideoFileClip(filename)