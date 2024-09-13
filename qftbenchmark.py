import qiskit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from utils import *
import os
import time
# from qiskit.utils import algorithm_globals
# from concurrent.futures import ThreadPoolExecutor


# consistent_seed_to_all_processes = 314159
# algorithm_globals.random_seed = consistent_seed_to_all_processes



FILE_NAME = "qft_benchmark.txt"
CPU_START_MEM = get_cpu_memory()

def benchmark_qft(num_qubits, timeout=17, time_sleep=0.01):
    # Create a QFT circuit
    qft_circuit = QFT(num_qubits=num_qubits, approximation_degree=0, do_swaps=True, 
        inverse=False, insert_barriers=True, name='QFT')
    qft_circuit.measure_all()

    # Simulate the QFT circuit
    backend = AerSimulator(device="GPU")
    transpiled_qft = qiskit.transpile(qft_circuit, backend)
    
    # file to write the results
    with open(FILE_NAME, "a") as f:
        f.write(f"{num_qubits:<20}")

    # Run the simulation
    pid = os.fork()
    if pid > 0:
        # monitor run time of the simulation
        # exc = ThreadPoolExecutor(max_workers=2)
        # backend.set_options(executor=exc)
        # backend.set_options(max_job_size=1)
        start_time = time.time()
        # result = backend.run(transpiled_qft, shots=1<<10).result()
        result = backend.run(transpiled_qft, shots=1<<10, 
                                blocking_enable=True, blocking_qubits=num_qubits).result()
        end_time = time.time()
        duration = end_time - start_time
        with open(FILE_NAME, "a") as f:
            f.write(f"{duration:<20.2f}")
        # print(f"QFT with {num_qubits} qubits took {duration:.2f} seconds")
        os.waitpid(pid, 0)
    else:
        gpu_mem_list, cpu_mem_list = monitor_memory(timeout=timeout, time_sleep=time_sleep)
        running_mem = max(gpu_mem_list)
        static_mem = gpu_mem_list[-1]
        mem_used = running_mem - static_mem
        with open(FILE_NAME, "a") as f:
            f.write(f"{mem_used:<20.2f}")
        # print(f"Max GPU Memory Used: {mem_used:.2f} MiB")
        running_mem = max(cpu_mem_list)
        # static_mem = cpu_mem_list[0]
        mem_used = running_mem - CPU_START_MEM
        with open(FILE_NAME, "a") as f:
            f.write(f"{mem_used:<20.2f}\n")
        os._exit(0)

if __name__ == "__main__":
    with open(FILE_NAME, "w") as f:
        # f.write("num_qubits\tduration(s)\t\tgpu_mem_used(MiB)\t\tcpu_mem_used(MiB)\n")
        f.write(f"{'num_qubits':<20}{'duration(s)':<20}{'gpu_mem_used(MiB)':<20}{'cpu_mem_used(MiB)':<20}\n")
    
    for i in range(1, 33):
        if i <= 20:
            timeout = 1
        elif i <= 29:
            timeout = 2
        else:
            timeout = 17
        benchmark_qft(num_qubits=i, timeout=timeout, time_sleep=0.01)
    # benchmark_qft(num_qubits=32, timeout=17, time_sleep=0.01)
    # print(os.environ["CUDA_VISIBLE_DEVICES"])
