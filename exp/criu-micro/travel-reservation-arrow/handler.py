

import sys
path_to_remove = '/home/ly/.local/lib/python3.12/site-packages'
sys.path = [p for p in sys.path if not p.rstrip('/').endswith(path_to_remove.rstrip('/'))]
sys.path.append("/home/ly/miniconda3/lib")
def get_input_old():
    return {
        "request_cnt": 10,
        "output":{
            "reserve_loc": "aaa",
            "reserve_date": "2025-10-10"
        }
    }

def get_input():
    return {"path1": "/tmp/functions/travel_loc.arrow", "path2": "/tmp/functions/travel_date.arrow"}


def warm_start_handler(params):
    import pyarrow as pa
    # import pandas
    file_path1 = params["path1"]
    file_path2 = params["path2"]
    import time
    s = time.time()
    result1 = {}
    result2 = {}
    with pa.memory_map(file_path1, 'r') as source:
        reader = pa.RecordBatchFileReader(source)
        table1 = reader.read_all()
    # return table1, {}
    #     # return table
    with pa.memory_map(file_path2, 'r') as source:
        reader = pa.RecordBatchFileReader(source)
        table2 = reader.read_all()

    return table1, table2
    


def lambda_handler(params, data):
    import random
    import json
    import time

    compute_time = 0
    start_time = time.time()
    
    table1, table2 = data
    for column in table1.itercolumns():
        key = column._name
        values = column.to_pylist()  # 转为 Python list
        result1[key] = values  # 即 [lat, lon]
    for column in table2.itercolumns():
        key = column._name
        values = column.to_pylist()  # 转为 Python list
        result2[key] = values  # 即 [lat, lon]
    # df1, df2 = warm_start_handler(params)
    # result1 = {col: df1[col].tolist() for col in df1.columns}
    # result2 = {col: df2[col].tolist() for col in df2.columns}
    end_random_time = time.time()
    commpute_time += end_random_time - start_random_time
    
    start_commnication_time = time.time()
    end_commnication_time = time.time()
    communication_time += end_commnication_time - start_commnication_time

    end_time = time.time()
    process_time = end_time - start_time
    
    return_val = {
        'communication_cnt': reserve_cnt,
        'process_time': process_time,
        'compute_time': commpute_time,
        'upload_time': communication_time,
        #'update': True,
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(return_val)
    }
    

if __name__ == "__main__":
    import time
    params = {"path1": "/tmp/functions/movie.arrow", "path2": "/tmp/functions/movie.arrow"}
    s = time.time()
    df1, df2 = warm_start_handler(params)
    e = time.time()
    print(e-s)
    # result1 = {col: df1[col].tolist() for col in df1.columns}
    # result2 = {col: df2[col].tolist() for col in df2.columns}
    # print(result1)
    # print(result2)
