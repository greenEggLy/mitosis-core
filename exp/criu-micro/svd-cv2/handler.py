
def warm_start_handler(params):
    import cv2
    img_path = params["img"]
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (300, 500))
    if img is None:
        raise FileNotFoundError(f"无法读取图片: {img_path}")
    return img

def lambda_handler(params, data):
    import numpy as np
    if data is None:
        raise ValueError("data 为空")
    print(f"data shape: {data.shape}, dtype: {data.dtype}")
    k = 50
    U, S, VT = np.linalg.svd(data, full_matrices=False)
    img_recon = np.dot(U[:, :k], np.dot(np.diag(S[:k]), VT[:k, :]))
    return img_recon


def get_input():
    params = {
        "img": "/tmp/test.jpg"
    }
    return params