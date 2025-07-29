import json
import pyarrow as pa
import time
import numpy as np

# 创建一个大型数据集
data = {
    'id': list(range(1, 1_000_001)),
    'values': np.random.rand(1_000_000).tolist(),
    'names': ['name_' + str(i) for i in range(1_000_000)]
}

# JSON序列化和反序列化
start = time.time()
json_data = json.dumps(data)
json_serialize_time = time.time() - start

start = time.time()
json.loads(json_data)
json_deserialize_time = time.time() - start

# Arrow序列化和反序列化
# 首先将数据转换为Arrow表格
arrays = [
    pa.array(data['id']),
    pa.array(data['values']),
    pa.array(data['names'])
]
arrow_table = pa.Table.from_arrays(arrays, names=['id', 'values', 'names'])

start = time.time()
sink = pa.BufferOutputStream()
with pa.RecordBatchStreamWriter(sink, arrow_table.schema) as writer:
    writer.write_table(arrow_table)
arrow_data = sink.getvalue()
arrow_serialize_time = time.time() - start

start = time.time()
with pa.BufferReader(arrow_data) as reader:
    arrow_table_loaded = pa.ipc.open_stream(reader).read_all()
arrow_deserialize_time = time.time() - start

# 打印结果对比
print(f"JSON 序列化时间: {json_serialize_time:.4f}秒")
print(f"JSON 反序列化时间: {json_deserialize_time:.4f}秒")
print(f"Arrow 序列化时间: {arrow_serialize_time:.4f}秒")
print(f"Arrow 反序列化时间: {arrow_deserialize_time:.4f}秒")