## setup

Strange that only qiskit-aer-gpu-cu11 is workable on this device, which has a cuda version of 12.3. Find out later, whether this is a problem to do with the configuration changed by myself, or to do with the qiskit-aer-gpu repo.

> qiskit-aer-gpu incurs a link error: undefined symbol: \_\_nvjitlinkgeterrorlog_12_6, version libnvjitlink.so.12

## task

- QFT: (from qiskit.circuit.library import QFT) limits qubit at 35
  > qiskit.transpiler.exceptions.CircuitTooWideForTarget: 'Number of qubits (128) in QFT is greater than maximum (35) in the coupling_map'

## performance

on single NVIDIA A100 80GB PCIe
monitoring with watch -n 1 nvidia-smi, or nvidia_smi.nvmlDeviceGetMemoryInfo(handle).
qubit=33: ERROR: std::bad_alloc'
