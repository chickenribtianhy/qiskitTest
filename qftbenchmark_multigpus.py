import qiskit
from qiskit_aer import AerSimulator
from qiskit.circuit.library import QFT
from utils import *
# import nvidia_smi
# import os
import time

def benchmark_qft(num_qubits, multi_gpu=False, precision="double"):
    # Create a QFT circuit
    qft_circuit = QFT(num_qubits=num_qubits, approximation_degree=0, do_swaps=True, 
        inverse=False, insert_barriers=True, name='QFT')
    qft_circuit.measure_all()

    # Simulate the QFT circuit
    backend = AerSimulator(device="GPU", precision=precision, batched_shots_gpu=multi_gpu)
    # print("Backend configuration:", backend.configuration())
    transpiled_qft = qiskit.transpile(qft_circuit, backend)
    
    # Run the simulation
    start_time = time.time()
    result = backend.run(transpiled_qft, shots=1<<10, 
                         blocking_enable=True, blocking_qubits=20).result()
    end_time = time.time()
    duration = end_time - start_time
    print(f"QFT with {num_qubits} qubits took {duration:.2f} seconds")
    counts = result.get_counts()
    # print(counts)
        
    

if __name__ == "__main__":
    # os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    # nvidia_smi.nvmlInit()
    # deviceCount = nvidia_smi.nvmlDeviceGetCount()
    # print(deviceCount)
    # benchmark_qft(num_qubits=34, multi_gpu=True, precision="single")
    benchmark_qft(num_qubits=33, multi_gpu=True, precision="double")

