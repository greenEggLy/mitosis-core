import random
import json
import pyarrow as pa

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

def save_as_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent = 2)
        
        
        
def save_as_arrow(data, filename):
    table = pa.Table.from_pylist(data)
    with pa.OSFile(filename, 'wb') as sink:
        with pa.RecordBatchFileWriter(sink, table.schema) as writer:
            writer.write_table(table)

            
            
if __name__ == "__main__":
    data = gen_random_data()
    save_as_json(data, "./movie.json")
    save_as_arrow(data, "./movie.arrow")
