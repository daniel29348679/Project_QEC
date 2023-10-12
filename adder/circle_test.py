# %%
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import qiskit.providers.aer.noise as noise
import matplotlib.pyplot as plt

# Error probabilities (from ibm_sherbrooke)
prob_1 = 0.00021932  # 1-qubit gate 0.0002193
prob_2 = 0.001  # 2-qubit gate 0.007395

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


def testcircle(numofqubit, totalxtime, coorrate, makeerror):
    if numofqubit < 3:
        print("numofqubit must >= 3 !!!!!!!!")

    circ = QuantumCircuit(numofqubit + 1, 1)
    #                                  sum qubit and support qubit

    for k in range(totalxtime):
        if makeerror:
            circ.x(range(numofqubit))
        circ.barrier()
        if k % coorrate == coorrate - 1:
            for i in range(numofqubit):
                fulladder(
                    circ, (i - 1) % numofqubit, i, (i + 1) % numofqubit, numofqubit
                )
                circ.reset(i)
                circ.cx(numofqubit, i)
                circ.reset(numofqubit)

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


def testcircle_rand(numofqubit, totalxtime, coorrate, makeerror):
    if numofqubit < 3:
        print("numofqubit must >= 3 !!!!!!!!")

    circ = QuantumCircuit(numofqubit + 1, 1)
    #                                  sum qubit and support qubit
    count = 0
    for k in range(totalxtime):
        if makeerror:
            circ.x(range(numofqubit))
        circ.barrier()
        if k % coorrate == coorrate - 1:
            for i in range(numofqubit):
                fulladder(
                    circ,
                    (i - 1 - count % 2) % numofqubit,
                    i,
                    (i + 1 + (count + 1) % 2) % numofqubit,
                    numofqubit,
                )
                circ.reset(i)
                circ.cx(numofqubit, i)
                circ.reset(numofqubit)
            if numofqubit > 3:
                for i in range(0, numofqubit, 2):
                    circ.swap(i, (i + 1) % numofqubit)
                for i in range(1, numofqubit, 2):
                    circ.swap(i, (i + 1) % numofqubit)
            count += 1

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
corrrate = 200  # 200
measurerate = 200  # 200
makeerror = True
totaltime = 2000  # 2000
x = range(0, totaltime, measurerate)

y1 = []
for i in x:
    y1.append(testcircle(3, i, corrrate, makeerror))
plt.plot(x, y1, color="r", label="corr")
for i in y1:
    print(i)

y1 = []
for i in x:
    y1.append(testcircle(6, i, corrrate, makeerror))
plt.plot(x, y1, color="g", label="corr")
for i in y1:
    print(i)


y1 = []
for i in x:
    y1.append(testcircle_rand(6, i, corrrate, makeerror))
    print(y1[-1])
plt.plot(x, y1, color="c", label="corr")

y2 = []
for i in x:
    y2.append(testcircle(3, i, 1000000, makeerror))
for i in y2:
    print(i)


plt.plot(x, y2, color="k", label="no corr")
plt.title(f"correct per {corrrate} x gates,{prob_1},{prob_2}")  # title
plt.ylabel("correct rate")  # y label
plt.xlabel("x gates")  # x label

plt.show()


# %%
