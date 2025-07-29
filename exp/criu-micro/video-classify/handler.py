
# serilize VideoFileClip
def serialize_video_file_clip(filename: str, vfc: VideoFileClip):
    import time
    from moviepy.video.io.VideoFileClip import VideoFileClip
    import utils
    from typing import Dict
    import shutil

    import random
    import logging

    assert isinstance(vfc, VideoFileClip)
    # filename = tmp_folder + 'tmp' + str(random.randint(0, 10 ** 10)) + '.mp4'
    # It seems ffmpeg is buggy when there are concurrent requests with the same file name.
    # We add a random number to the file name to avoid this.
    vfc.write_videofile(filename, logger=None)

# deserialize VideoFileClip
def deserialize_video_file_clip(tmp_folder: str, bits: bytes):
    import time
    from moviepy.video.io.VideoFileClip import VideoFileClip
    import utils
    from typing import Dict
    import shutil

    import random
    import logging

    assert isinstance(bits, bytes)
    filename = tmp_folder + 'tmp' + str(random.randint(0, 10 ** 10)) + '.mp4'
    with open(filename, 'wb') as f:
        f.write(bits)
    return VideoFileClip(filename)

def get_input():
    return {
        'file_nums': 1, 
        'input': {
            'pattern': "video_[file_id].MOV"  # Pattern for input file names, e.g., "video_[file_id].mp4"
        },
        'chunk_size': 2,  # Size of each video chunk in seconds
        'folder': "./utils/",
        'tmp_folder': "./tmp/",
        'output': {
            'pattern': 'out_video_[file_id]_[chunk_id].mp4'
        }
    }

def lambda_handler(input):
    import time
    from moviepy.video.io.VideoFileClip import VideoFileClip
    import utils
    from typing import Dict
    import shutil

    import random
    import logging

    file_nums = int(input['file_nums'])
    input_pattern = input['input']['pattern']
    chunk_size = int(input['chunk_size'])
    output_pattern = input['output']['pattern']
    if input['folder'][-1] != '/':
        input['folder'] += '/'
    folder = input['folder']
    tmp_folder = input['tmp_folder']
    # chknum_path = input['output']['chknum_path']
    
    start = time.time()
    read_time = 0
    write_time = 0
    comp_time = 0

    chunks_num: Dict[int, int] = {}
    
    for idx in range(file_nums):
        file_name = input_pattern.replace('[file_id]', str(idx))
        
        read_time -= time.time()
        tmp_filename = tmp_folder + file_name
        src_filename = folder + file_name
        print(f"file name: {tmp_filename}")
        shutil.copy(src_filename, tmp_filename)

        start_comp = time.time()
        # vc = VideoFileClip(tmp_filename, verbose=False)
        vc = VideoFileClip(tmp_filename)
        video_len = int(vc.duration)
        read_time += time.time()
        print(f"video length: {video_len}")
        
        start_size = 0
        cnt = 0
        end_comp = time.time()
        comp_time += end_comp - start_comp
        
        while start_size < video_len:
            start_comp = time.time()
            end_size = min(start_size + chunk_size, video_len)
            
            clip_vc = vc.subclipped(start_size, end_size)
            end_comp = time.time()
            comp_time += end_comp - start_comp
            
            start_write = time.time()

            clip_name = output_pattern.replace('[file_id]', str(idx)) \
                .replace('[chunk_id]', str(cnt))
            tmp_filename = tmp_folder + clip_name
            serialize_video_file_clip(tmp_filename, clip_vc)

            # md.output(['extract'], clip_name, serialize_video_file_clip(folder, clip_vc))
            
            cnt += 1
            start_size += chunk_size
            end_write = time.time()
            write_time += end_write - start_write
        
        chunks_num[idx] = cnt

        vc.close()

    write_time -= time.time()
    # md.output(['extract', 'preprocess', 'classify'], chknum_path, chunks_num)
    write_time += time.time()

    end = time.time()
    
    return {
        'input_time': read_time, 
        'compute_time': comp_time, 
        'output_time': write_time, 
        'total_time': end - start
    }
