import orjson
import gzip

def warm_start_handler(params):
    filename = params["file_name"]
    with gzip.open(filename, "rt", encoding="utf-8") as f:
        data = f.read()
        return orjson.loads(data)

def lambda_handler(params,data):
    return data


def get_input():
    params = {
        "file_name": "/tmp/com_data.json.gz"
    }
    return params