# %%
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import qiskit.providers.aer.noise as noise

# Error probabilities (from ibm_sherbrooke)
prob_1 = 0.0  # 1-qubit gate 0.0002193
prob_2 = 0.01  # 2-qubit gate 0.007395

error_1 = noise.depolarizing_error(prob_1, 1)
error_2 = noise.depolarizing_error(prob_2, 2)

noise_model = noise.NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1, ["u1", "u2", "u3"])
noise_model.add_all_qubit_quantum_error(error_2, ["cx"])

basis_gates = noise_model.basis_gates

shots = 10000


def ccx(circuit, a, b, c):
    circuit.barrier()
    circuit.h(c)
    circuit.cx(b, c)
    circuit.tdg(c)
    circuit.cx(a, c)
    circuit.t(c)
    circuit.cx(b, c)
    circuit.tdg(c)
    circuit.cx(a, c)
    circuit.t(c)
    circuit.h(c)
    circuit.barrier()


# %% Make a circuit
circ = QuantumCircuit(3, 3)
circ.x([0, 1])
ccx(circ, 0, 1, 2)


circ.measure([0, 1, 2], [2, 1, 0])
circ.draw("mpl")

# %% Make a circuit
circ = QuantumCircuit(2, 2)
circ.cx(0, 1)


circ.measure([0, 1], [1, 0])
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
plot_histogram(counts)
# %%
