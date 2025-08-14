
def warm_start_handler(params):
    import orjson
    file_name = params["file_name"]
    with open(file_name, "rb") as f:
        return orjson.loads(f.read())


def lambda_handler(params,data):
    return data


def get_input():
    params = {
        "file_name": "/tmp/com_data.json"
    }
    return params