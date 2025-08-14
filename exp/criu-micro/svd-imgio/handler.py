

def warm_start_handler(params):
    import imageio.v2 as imageio
    import numpy as np
    img_path = params["img"]
    k = 50
    img = imageio.imread(img_path)
    if img.ndim == 3:  # RGB转灰度
        img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    return img



def lambda_handler(params, data):
    import numpy as np
    # import imageio.v2 as imageio
    # img_path = params["img"]
    k = 50
    img = data
    # img = imageio.imread(img_path)
    # if img.ndim == 3:  # RGB转灰度
    #     img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    
    # SVD 分解
    U, S, VT = np.linalg.svd(img, full_matrices=False)
    # 保留前 k 个奇异值
    img_recon = np.dot(U[:, :k], np.dot(np.diag(S[:k]), VT[:k, :]))
    return img_recon


def get_input():
    params = {
        "img": "/tmp/test.jpg"
    }
    return params