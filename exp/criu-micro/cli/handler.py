import json
import time


def get_input():
    return {"output": {}, "user_num": 1000000, "path": "./utils/data.json"}


def lambda_handler(params):
    start_time = time.time()
    oa = params["output"]
    user_num = params["user_num"]  # 1000000
    path = params["path"]

    start_compute_time = time.time()
    with open(path, "r", encoding="utf-8") as file:
        file_content = file.read()
        data = json.loads(file_content)
    movie_data = {movie_info["Title"]: movie_info["MovieId"] for movie_info in data}
    user_data = {f"username_{idx}": idx for idx in range(user_num)}
    com_data = {"movie": movie_data, "user": user_data}
    com_data_recommend = {"movie": data, "user": user_data}

    end_compute_time = time.time()
    start_output_time = time.time()
    # md.output(['stage2'], f'{oa}-2', com_data)
    # md.output(['stage3'], f'{oa}-3', com_data)
    # md.output(['stage4'], f'{oa}-4', com_data_recommend)
    # md.output(['stage5'], f'{oa}-5', com_data_recommend)

    end_output_time = time.time()
    end_time = time.time()

    return_val = {
        "process_time": end_time - start_time,
        "input_time": 0,
        "compute_time": end_compute_time - start_compute_time,
        "output_time": end_output_time - start_output_time,
    }

    return {"statusCode": 200, "body": json.dumps(return_val)}
