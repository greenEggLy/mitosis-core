
import sys
path_to_remove = '/home/ly/.local/lib/python3.12/site-packages'
sys.path = [p for p in sys.path if not p.rstrip('/').endswith(path_to_remove.rstrip('/'))]
def get_input():
    return {"output": {}, "user_num": 1000000, "path": "./utils/movie.json"}

def gen_random_data(num_movies = 1_000_000):
    movies = []
    for i in range(num_movies):
        movie = {
            "Title": f"Movie {i + 1}",
            "MovieId": random.randint(1000, 9999),
            "Genre": random.choice(["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]),
            "Year": random.randint(1980, 2023),
        }
        movies.append(movie)
    return movies
    
def warm_start_handler(params):
    import json
    import time
    start = time.time()
    path = params["path"]
    with open(path, "r", encoding="utf-8") as file:
        file_content = file.read()
        data = json.loads(file_content)

    end = time.time()
    print(f"Deserialize json data time: {end-start}")
    return data


def lambda_handler(params):
    import time
    import json
    # print(str(pa.cpp_version_info))
    start_time = time.time()
    oa = params["output"] 
    user_num = params["user_num"]  # 1000000
    start_compute_time = time.time()
    data = gen_random_data()
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
