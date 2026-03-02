"""
1.用corr(fulladder + reset + cx 回寫)去跑兩種環狀 qubit 系統
2.掃不同的時間長度(totalxtime = i),把「最後q0是維持0的比例」當作 correct rate,畫成曲線(correct rate vs x gates)
3.output圖中的correct rate不是「整體電路正確率」,只看q0最後是不是0
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import qiskit_aer.noise as noise  # 新的匯入路徑比較穩
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# 設定 physical error rate
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
def fulladder(circuit, a, b, c, carry):
    """only carry()!!no sum!!但carry就很像majority的邏輯"""
    circuit.ccx(a, b, carry)
    circuit.cx(a, b)
    circuit.ccx(b, c, carry)
    circuit.cx(a, b)

# 固定鄰居的環狀局部糾錯，固定用0<-(-1,0,1)
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
    backend = Aer.get_backend("aer_simulator")
    tcirc = transpile(circ, backend, basis_gates=basis_gates, optimization_level=0)

    result = backend.run(
        tcirc,
        shots=shots,
        noise_model=noise_model
    ).result()

    counts = result.get_counts()
    return counts.get("0", 0) / shots

# 鄰居選擇交錯 + swap，「把錯誤/資訊更均勻地攪散」會不會讓局部糾錯更有效?
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
corrrate = 200  # 200
measurerate = 200  # 200
makeerror = False
totaltime = 2000  # 2000
x = range(0, totaltime, measurerate)

print("3 bit")
y1 = []
for i in x:
    y1.append(testcircle(3, i, corrrate, makeerror))
plt.plot(x, y1, color="r", label="3bit testcircle")
for i in y1:
    print(i)

print("6 bit")
y1 = []
for i in x:
    y1.append(testcircle(6, i, corrrate, makeerror))
plt.plot(x, y1, color="g", label="6bit testcircle")
for i in y1:
    print(i)

print("6 bit rand")
y1 = []
for i in x:
    y1.append(testcircle_rand(6, i, corrrate, makeerror))
    print(y1[-1])
plt.plot(x, y1, color="c", label="6bit testcircle_rand")

print("base")
y2 = []
for i in x:
    y2.append(testcircle(3, i, 1000000, makeerror))
for i in y2:
    print(i)


plt.plot(x, y2, color="k", label="no corr")


plt.title(f"correct per {corrrate} x gates,{prob_1},{prob_2}")  # title
plt.ylabel("correct rate")  # y label
plt.xlabel("x gates")  # x label
plt.legend()
plt.show()
