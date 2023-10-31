# %%
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import qiskit.providers.aer.noise as noise

# Error probabilities (from ibm_sherbrooke)
prob_1 = 0.0002193  # 1-qubit gate 0.0002193
prob_2 = 0.007395  # 2-qubit gate 0.007395

error_1 = noise.depolarizing_error(prob_1, 1)
error_2 = noise.depolarizing_error(prob_2, 2)

noise_model = noise.NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1, ["u1", "u2", "u3"])
noise_model.add_all_qubit_quantum_error(error_2, ["cx"])

basis_gates = noise_model.basis_gates

shots = 1000


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


circ = QuantumCircuit(16, 4)

docorr = 1
totaltime = 1
xtimepercorr = 0

for k in range(totaltime):
    for i in range(xtimepercorr):
        circ.x([0, 1, 2])
        circ.barrier()
    if docorr:
        corr(circ)


# corr(circ)
circ.measure([0, 1, 2, 15], [0, 1, 2, 3])
circ.draw("mpl")
# %%
# run the noisy simulation
result = execute(
    circ,
    Aer.get_backend("qasm_simulator"),
    basis_gates=basis_gates,
    noise_model=noise_model,
    shots=shots,
).result()
counts = result.get_counts(0)
print(f"correct rate: {(counts['0000'])/shots:.4f}")
print(f"uncorrect rate: {1-(counts['0000'])/shots:.4f}")
plot_histogram(counts)
# %%
