# %%
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import qiskit.providers.aer.noise as noise
import matplotlib.pyplot as plt

# Error probabilities (from ibm_sherbrooke)
prob_1 = 0.0002193  # 1-qubit gate 0.0002193
prob_2 = 0.0002193  # 0.007395  # 2-qubit gate 0.007395

error_1 = noise.depolarizing_error(prob_1, 1)
error_2 = noise.depolarizing_error(prob_2, 2)

noise_model = noise.NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1, ["u1", "u2", "u3"])
noise_model.add_all_qubit_quantum_error(error_2, ["cx"])

basis_gates = noise_model.basis_gates

shots = 10000


# %% Make a circuit
def fulladder(circuit, in1, in2, in3, carry):
    """in1, in2, in3 are the input qubits, carry is the output qubit,!!no sum"""
    circuit.ccx(in1, in2, carry)
    circuit.cx(in1, in2)
    circuit.ccx(in2, in3, carry)
    circuit.cx(in1, in2)


def corr(circuit):
    circuit.barrier()
    fulladder(circuit, 0, 1, 2, 9)
    fulladder(circuit, 3, 4, 5, 10)
    fulladder(circuit, 6, 7, 8, 11)

    circuit.cx([0, 9], 12)
    circuit.cx(12, 0)
    circuit.reset(12)
    circuit.cx([1, 9], 12)
    circuit.cx(12, 1)
    circuit.reset(12)
    circuit.cx([2, 9], 12)
    circuit.cx(12, 2)
    circuit.reset(12)

    circuit.cx([3, 10], 12)
    circuit.cx(12, 3)
    circuit.reset(12)
    circuit.cx([4, 10], 12)
    circuit.cx(12, 4)
    circuit.reset(12)
    circuit.cx([5, 10], 12)
    circuit.cx(12, 5)
    circuit.reset(12)

    circuit.cx([6, 11], 12)
    circuit.cx(12, 3)
    circuit.reset(12)
    circuit.cx([7, 11], 12)
    circuit.cx(12, 4)
    circuit.reset(12)
    circuit.cx([8, 11], 12)
    circuit.cx(12, 5)
    circuit.reset(12)

    circuit.reset([9, 10, 11])


def doubleqec_9(totalxtime, coorrate):
    circ = QuantumCircuit(13, 1)

    for k in range(0, totalxtime):
        circ.x(range(9))
        circ.barrier()
        if k % coorrate == coorrate - 1:
            corr(circ)

    circ.measure([0], [0])

    result = execute(
        circ,
        Aer.get_backend("qasm_simulator"),
        basis_gates=basis_gates,
        noise_model=noise_model,
        shots=shots,
    ).result()
    counts = result.get_counts(0)

    return counts["0"] / shots


# %%
corrrate = 100
x = range(0, 500, corrrate)
y1 = []

for i in x:
    y1.append(doubleqec_9(i, 100))
    print(i)
# %%
plt.plot(x, y1, color="r", label="corr")
ybase = [1.0, 0.9914, 0.9812, 0.9675, 0.9563, 0.9496, 0.9396, 0.9288, 0.92, 0.9093]
y2 = ybase[0 : len(y1)]
plt.plot(x, y2, color="g", label="no corr")

plt.title(f"doubleqec\ncorrect per {corrrate} x gates,{prob_1},{prob_2}")  # title
plt.ylabel("correct rate")  # y label
plt.xlabel("x gates")  # x label

plt.show()

# %%
