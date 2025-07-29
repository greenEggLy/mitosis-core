import numpy as np

def generate_random_data(num_samples=100, num_features=5, filename='random_data.txt'):
    # 随机生成标签（0或1）
    labels = np.random.randint(0, 2, size=(num_samples, 1))
    
    # 随机生成特征值
    features = np.random.rand(num_samples, num_features) * 10  # 生成0到10之间的随机数
    
    # 将标签和特征值拼接在一起
    data = np.concatenate((labels, features), axis=1)
    
    # 保存到文件，以制表符分隔
    np.savetxt(filename, data, delimiter='\t', fmt='%.2f')

    print(f"随机数据已生成并保存到 {filename}")

# 调用函数生成数据
generate_random_data(num_samples=100, num_features=5, filename='random_data.txt')
