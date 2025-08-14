def warm_start_handler(params):
    text = params["text"]
    return text.lower().split()

def lambda_handler(params, data):
    from collections import Counter
    words = data
    counter = Counter(words)
    # 按频率从高到低排序
    stats = []
    for word, count in counter.most_common():
        print(f"{word}: {count}")
        stats.append({word: str(count)})


def get_input():
    params = {
        "text": "Hello hahaha apple king never hahaha bad apple" * 500000
    }
    return params
