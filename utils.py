import time
import psutil
import nvidia_smi

def get_gpu_memory():
    """Retrieve GPU memory usage via nvidia-smi."""
    # result = os.run(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,nounits,noheader'],
    #                         capture_output=True, text=True)
    # memory_info = result.stdout.strip().split('\n')
    nvidia_smi.nvmlInit()
    deviceCount = nvidia_smi.nvmlDeviceGetCount()
    mem_used = []
    for i in range(deviceCount):
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
        util = nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
        mem = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        mem_used.append(mem.used / 1024**2)
        # print(mem_used)
        # print(f"|Device {i}| Mem Used: {mem.used/1024**2:5.2f}MB / {mem.total/1024**2:5.2f}MB | gpu-util: {util.gpu:3.1%} | gpu-mem: {util.memory:3.1%} |")
    # print(mem_used)
    return mem_used
    
    # return int(memory_info[0])
def get_cpu_memory():
    """Retrieve CPU memory usage via psutil."""
    memory_info = psutil.virtual_memory().used
    # print(memory_info)
    return memory_info / (1024 ** 2)

def monitor_memory(timeout=10, time_sleep=0.01, multi_gpu=False):
    gpu_mem_list = []
    gpu_mem_list2 = []
    cpu_mem_list = []

    while timeout > 0:
        gpu_mem = get_gpu_memory()
        gpu_mem_list.append(gpu_mem[0])
        if multi_gpu:
            gpu_mem_list2.append(gpu_mem[1])
        cpu_mem = get_cpu_memory()
        cpu_mem_list.append(cpu_mem)
        timeout -= time_sleep
        time.sleep(time_sleep)
    if multi_gpu:
        return gpu_mem_list, gpu_mem_list2, cpu_mem_list
    return gpu_mem_list, cpu_mem_list

