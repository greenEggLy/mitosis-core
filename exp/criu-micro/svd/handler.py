

def lambda_handler(params):
    import numpy as np
    from PIL import Image
    img_path = params["img"]

    def load_grayscale_image(path):
        img = Image.open(path).convert('L')
        return np.array(img)

    def svd_compress(image_matrix, k):
        U, S, VT = np.linalg.svd(image_matrix, full_matrices=False)
        S_k = np.diag(S[:k])
        U_k = U[:, :k]
        VT_k = VT[:k, :]
        
        compressed_image = np.dot(U_k, np.dot(S_k, VT_k))
        return compressed_image

    img_matrix = load_grayscale_image(img_path)

    k = 50
    compressed_img = svd_compress(img_matrix, k)
    return compressed_img


def get_input():
    params = {
        "img": "/tmp/test.png"
    }
    return params