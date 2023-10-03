# %%
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import qiskit.providers.aer.noise as noise
import matplotlib.pyplot as plt

# Error probabilities (from ibm_sherbrooke)
prob_1 = 0.0002193  # 1-qubit gate 0.0002193
prob_2 = 0.0002193  # 2-qubit gate 0.007395

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


def testcirc(totalxtime, coorrate):
    circ = QuantumCircuit(9, 3)

    for k in range(totalxtime):
        circ.x([0, 1, 2])
        circ.barrier()
        if k % coorrate == coorrate - 1:
            corr(circ)

    circ.measure([0, 1, 2], [0, 1, 2])
    result = execute(
        circ,
        Aer.get_backend("qasm_simulator"),
        basis_gates=basis_gates,
        noise_model=noise_model,
        shots=shots,
    ).result()
    counts = result.get_counts(0)
    sum = counts["000"]
    if "100" in counts:
        sum += counts["100"]
    if "010" in counts:
        sum += counts["010"]
    if "001" in counts:
        sum += counts["001"]
    # print(sum)
    return sum / shots


# %%
corrrate = 100
x = range(0, 1000, corrrate)
y1 = []
for i in x:
    y1.append(testcirc(i, corrrate))
    print(i)

y2 = []
for i in x:
    y2.append(testcirc(i, 1000000))

# %%
plt.plot(x, y1, color="r", label="corr")
plt.plot(x, y2, color="g", label="no corr")
plt.title(f"correct per {corrrate} x gates,{prob_1},{prob_2}")  # title
plt.ylabel("correct rate")  # y label
plt.xlabel("x gates")  # x label

plt.show()


# %%
