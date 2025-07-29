#!/usr/bin/env python3
import docker
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import argparse
import os

class DockerMountBenchmark:
    def __init__(self, container_count=3, image="ly/mitosis:v3", prefix="test", mount_dir="/tmp/functions"):
        self.client = docker.from_env()
        self.container_count = container_count
        self.image = image
        self.prefix = prefix
        self.mount_dir = mount_dir
        self.containers = []
        
        os.makedirs(self.mount_dir, exist_ok=True)
        
    def setup_containers(self, case):
        """创建并配置测试容器"""
        print(f"正在创建 {self.container_count} 个测试容器...")
        
        self.cleanup()
        

        test_script_path = os.path.join(self.mount_dir, "test.py")
        if case == "movie":
            with open(test_script_path, "w") as f:
                f.write("""
def main():
    import json
    import time
    path = \"/mnt/functions/movie.json\"
    with open(path, 'r') as file:
        file_content = file.read()
        data = json.loads(file_content)
    return data

if __name__ == "__main__":
    main()
""")
        else:
            with open(test_script_path, "w") as f:
                f.write("""
def main():
    import json
    import time
    s = time.time()
    path1 = \"/tmp/functions/travel_date.json\"
    path2 = \"/tmp/functions/travel_loc.json\"
    with open(path1, 'r') as file:
        file_content = file.read()
        data1 = json.loads(file_content)
    with open(path2, 'r') as file:
        file_content = file.read()
        data2 = json.loads(file_content)
    e = time.time()
    print(e-s)
    return data1, data2

if __name__ == "__main__":
    main()
""")
        
        os.chmod(test_script_path, 0o755)  # 确保脚本有执行权限
        for i in range(1, self.container_count + 1):
            container = self.client.containers.run(
                self.image,
                name=f"{self.prefix}_{i}",
                command=f"sleep infinity",  # 容器启动后执行的命令
                detach=True,
                volumes={
                    self.mount_dir: {
                        'bind': '/mnt/functions',
                        'mode': 'ro'  # 只读挂载
                    }
                }
            )
            self.containers.append(container)
            container.pause()
            container.reload()
            print(f"{container.name}当前状态: {container.status}")
        
    def cleanup(self):
        """清理测试容器"""
        for container in self.client.containers.list(all=True):
            if container.name.startswith(self.prefix):
                try:
                    container.stop()
                    container.remove()
                    # print(f"已清理容器 {container.name}")
                except Exception as e:
                    print(f"清理容器 {container.name} 失败: {e}")
    
    def test_serial(self):
        """串行测试容器启动和执行时间"""
        print("\n=== 串行测试 ===")
        start_times = []
        exec_times = []
        
        for container in self.containers:
            start = time.perf_counter()
            container.unpause()
            unpause_time = time.perf_counter()
            exit_code, output = container.exec_run("python /mnt/functions/test.py")
            if exit_code == 0:
                print(f"{container.name}: {output}")
            else:
                print(f"{container.name} exit code: {exit_code}")
            
            end = time.perf_counter()
            all_time = end - start
            
            exec_time = end - unpause_time
            all_time = end - start
            
            if exec_time is not None:
                exec_times.append(exec_time)
                print(f"{container.name}: 总耗时 {all_time:.2f} 秒 (脚本执行: {exec_time:.2f} 秒)")
            else:
                print(f"{container.name}: 总耗时 {all_time:.2f} 秒 (未能获取脚本执行时间)")
            
            container.stop()
        
        # 输出统计结果
        if start_times:
            print("\n串行测试结果:")
            print(f"平均启动+执行时间: {statistics.mean(start_times):.2f} 秒")
            print(f"平均脚本执行时间: {statistics.mean(exec_times):.2f} 秒")
            print(f"最大总耗时: {max(start_times):.2f} 秒")
    
    def _test_single_container(self, container):
        start = time.perf_counter()
        container.unpause()
        unpause_time = time.perf_counter()
        # print(f"{container.name} unpause time {unpause_time}")
        exit_code, output = container.exec_run("python /mnt/functions/test.py")
        if exit_code != 0:
            print(f"{container.name} exit code: {exit_code}")
        
        end = time.perf_counter()
        exec_time = end - unpause_time
        elapsed = end - start
        
        container.stop()
        
        return {
            "name": container.name,
            "total_time": elapsed,
            "exec_time": exec_time,
            "output": output
        }
    
    def test_parallel(self, workers=4):
        """并行测试容器启动和执行时间"""
        print(f"\n=== 并行测试 (workers={workers}) ===")
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(self._test_single_container, self.containers))
        
        total_times = []
        exec_times = []
        
        for result in results:
        #     print(f"\n{result['name']} 结果:")
        #     for line in result['output']:
        #         print(f"  {line}")
        #     print(f"  总耗时: {result['total_time']:.2f} 秒")
            
            if result['exec_time'] is not None:
            #     print(f"  脚本执行时间: {result['exec_time']:.2f} 秒")
                exec_times.append(result['exec_time'])
            
            total_times.append(result['total_time'])
        
        # 输出统计结果
        if total_times:
            print("\n并行测试结果:")
            print(f"mean unpause time: {statistics.mean(total_times):.2f} 秒")
            # print(f"平均脚本执行时间: {statistics.mean(exec_times):.2f} 秒")
            print(f"max unpause time: {max(total_times):.2f} 秒")
    
    def run(self, case, mode="both", parallel_workers=4):
        """运行测试"""
        self.setup_containers(case)
        
        if mode in ["serial", "both"]:
            self.test_serial()
        
        if mode in ["parallel", "both"]:
            # 重置容器状态
            for container in self.containers:
                if container.status == "running":
                    container.pause()
                # container.unpause()  # 重新创建容器会丢失状态，所以这里只需要启动
            
            self.test_parallel(workers=parallel_workers)
        
        self.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Docker容器挂载目录并执行Python脚本测试")
    parser.add_argument("--count", type=int, default=3, help="测试容器数量")
    parser.add_argument("--image", default="ly/mitosis:v3", help="使用的Docker镜像")
    parser.add_argument("--prefix", default="test", help="容器名前缀")
    parser.add_argument("--mount", default="/tmp/functions", help="要挂载的本地目录路径")
    parser.add_argument("--mode", choices=["serial", "parallel", "both"], default="both",
                      help="测试模式: serial(串行), parallel(并行), both(两者)")
    parser.add_argument("--workers", type=int, default=4,
                      help="并行测试时的worker数量")
    parser.add_argument("--case", choices=["movie", "travel"])
    
    args = parser.parse_args()
    
    benchmark = DockerMountBenchmark(
        container_count=args.count,
        image=args.image,
        prefix=args.prefix,
        mount_dir=args.mount
    )
    
    benchmark.run(
        case = args.case,
        mode=args.mode,
        parallel_workers=args.workers
    )