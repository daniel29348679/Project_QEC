# %%
from qiskit import *
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

simulator = Aer.get_backend("aer_simulator")


# %% Make a circuit
def fulladder(circuit, in1, in2, in3, carry):
    """in1, in2, in3 are the input qubits, carry is the output qubit,!!no sum"""
    circuit.ccx(in1, in2, carry)
    circuit.cx(in1, in2)
    circuit.ccx(in2, in3, carry)
    circuit.cx(in1, in2)


def corr(circuit):
    circuit.barrier()
    fulladder(circuit, 0, 1, 2, 3)
    circuit.barrier()
    fulladder(circuit, 0, 1, 2, 4)
    circuit.barrier()
    fulladder(circuit, 0, 1, 2, 5)
    circuit.barrier()
    circuit.cx([0, 3], 6)
    circuit.cx(6, 0)
    circuit.barrier()
    circuit.cx([1, 4], 7)
    circuit.cx(7, 1)
    circuit.barrier()
    circuit.cx([2, 5], 8)
    circuit.cx(8, 2)
    circuit.barrier()
    circuit.reset([3, 4, 5, 6, 7, 8])


circ = QuantumCircuit(16, 3)
circ.initialize("011", [0, 1, 2])
circ.barrier()
corr(circ)
# circ.reset([0, 1, 2])
circ.measure([0, 1, 2], [0, 1, 2])
circ.draw("mpl")
#%%

circ = transpile(circ, simulator)

result = simulator.run(circ).result()
counts = result.get_counts(circ)
plot_histogram(counts)
# %%
