## setup

Strange that only qiskit-aer-gpu-cu11 is workable on this device, which has a cuda version of 12.3. Find out later, whether this is a problem to do with the configuration changed by myself, or to do with the qiskit-aer-gpu repo.

> qiskit-aer-gpu incurs a link error: undefined symbol: \_\_nvjitlinkgeterrorlog_12_6, version libnvjitlink.so.12

## task

- QFT: from qiskit.circuit.library import QFT

## performance

on single NVIDIA A100 80GB PCIe
monitoring with watch -n 1 nvidia-smi, or nvidia_smi.nvmlDeviceGetMemoryInfo(handle).
qubit=33: ERROR: std::bad_alloc'

Qiskit uses double-precision, 16B per complex number
reduce to single-precision should increase the workable qubit by 1
Verified: GPU memory 66251MiB / 81920MiB for qubit=33

## multiple gpu

- qiskit-aer multi-gpu

set batched_shots_gpu=True when initializing a simulator/backend
https://qiskit.github.io/qiskit-aer/howtos/running_gpu.html#running-with-multiple-gpus-and-or-multiple-nodes
