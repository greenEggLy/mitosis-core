

import sys
path_to_remove = '/home/ly/.local/lib/python3.12/site-packages'
sys.path = [p for p in sys.path if not p.rstrip('/').endswith(path_to_remove.rstrip('/'))]

def get_input():
    return {"output": {}, "user_num": 1000000, "path": "./utils/movie.arrow"}

    
def warm_start_handler(params):
    import pyarrow as pa
    file_path = params["path"]
    try:
        with pa.memory_map(file_path, 'r') as source:
            reader = pa.RecordBatchFileReader(source)
            table = reader.read_all()
            return table
    
    except Exception as e:
        raise



def lambda_handler(params, data):
    import json
    import time
    start_time = time.time()
    oa = params["output"]
    user_num = params["user_num"]  # 1000000
    start_compute_time = time.time()
    titles = data.column("Title").to_pylist()
    movie_infos = data.column("MovieId").to_pylist()
    movie_data = {title: movie_info for (title, movie_info) in zip(titles, movie_infos)}
    user_data = {f"username_{idx}": idx for idx in range(user_num)}
    com_data = {"movie": movie_data, "user": user_data}
    com_data_recommend = {"movie": data, "user": user_data}

    end_compute_time = time.time()
    start_output_time = time.time()

    end_output_time = time.time()
    end_time = time.time()

    return_val = {
        "process_time": end_time - start_time,
        "input_time": 0,
        "compute_time": end_compute_time - start_compute_time,
        "output_time": end_output_time - start_output_time,
    }

    return {"statusCode": 200, "body": json.dumps(return_val)}
