

def lambda_handler(params):
    import re
    from collections import Counter
    text = params["text"].lower()
    words = re.findall(r'\b\w+\b', text)  # 使用正则提取单词

    counter = Counter(words)
    # 按频率从高到低排序
    stats = []
    for word, count in counter.most_common():
        print(f"{word}: {count}")
        stats.append({word: str(count)})


def get_input():
    params = {
        "text": "Hello hahaha apple, king never hahaha, bad apple"
    }
    return params
