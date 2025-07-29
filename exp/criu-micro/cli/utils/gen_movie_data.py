import json
import random


def generate_random_movie_data(num_movies):
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


def save_to_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    num_movies = 10  # 生成的电影数量
    movie_data = generate_random_movie_data(num_movies)
    save_to_json("movie-review/data.json", movie_data)
