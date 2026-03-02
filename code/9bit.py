"""
模擬量子電路在不同電路長度下的正確率衰減,發現使用QEC後可減緩衰減情況
保護9個data qubit(q0~q8),而且分成三個 block,3組3-bit repetition
三個三個一組,分別寫到9,10,11
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import qiskit_aer.noise as noise  # 新的匯入路徑比較穩
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# 設定 physical error rate
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
def fulladder(circuit, a, b, c, carry):
    """only carry()!!no sum!!但carry就很像majority的邏輯"""
    circuit.ccx(a, b, carry)
    circuit.cx(a, b)
    circuit.ccx(b, c, carry)
    circuit.cx(a, b)


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

    backend = Aer.get_backend("aer_simulator")
    tcirc = transpile(circ, backend, basis_gates=basis_gates, optimization_level=0)

    result = backend.run(
        tcirc,
        shots=shots,
        noise_model=noise_model
    ).result()

    counts = result.get_counts()
    return counts.get("0", 0) / shots


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
plt.legend()
plt.show()

# %%
