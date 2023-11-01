# %%
import numpy as np
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt


class boolcirc:
    def __init__(self, qubit, errorrate):
        self.qubit = np.array([False] * qubit, dtype=np.bool_)
        self.prob = errorrate

    def checkerror(self, i, rate):
        if np.random.rand() < self.prob * rate:
            self.qubit[i] = not self.qubit[i]

    def checkerror_both(self, i, j, rate):
        if np.random.rand() < self.prob * rate:
            self.qubit[i] = not self.qubit[i]
            self.qubit[j] = not self.qubit[j]

    def checkerror_ecr(self, i, j):
        self.checkerror(i, 0.25)
        self.checkerror(j, 0.25)
        self.checkerror_both(i, j, 0.25)

    def reset(self, a):
        self.qubit[a] = False

    def x(self, a):
        self.qubit[a] = not self.qubit[a]

    def cx(self, a, b):
        if self.qubit[a]:
            self.qubit[b] = not self.qubit[b]
        self.checkerror_ecr(a, b)

    def ccx(self, c1, c2, t):
        beginstate = self.qubit[c1] ^ self.qubit[c2]

        self.checkerror_ecr(c1, t)
        self.checkerror_ecr(c2, t)
        self.checkerror_ecr(c1, t)
        self.checkerror_ecr(c2, t)

        if self.qubit[c1] and self.qubit[c2]:
            self.qubit[t] = not self.qubit[t]

        self.qubit[t] ^= beginstate ^ self.qubit[c1] ^ self.qubit[c2]

    def swap(self, a, b):
        self.cx(a, b)
        self.cx(b, a)
        self.cx(a, b)

    def count(self, f, e, value):
        count = 0
        for i in range(f, e):
            if self.qubit[i] == value:
                count += 1
        return count

    def __str__(self):
        s = ""
        for i in self.qubit:
            if i:
                s += "1"
            else:
                s += "0"
        return s


"""
errorrate = 0.01
shots = 10000
counts = {}
for _ in range(shots):
    circ = boolcirc(3, errorrate)
    circ.x(0)
    circ.x(1)
    circ.ccx(0, 1, 2)
    if str(circ) not in counts:
        counts[str(circ)] = 0
    counts[str(circ)] += 1

plot_histogram(counts)
"""


prob_2 = 0.007395  # 2-qubit gate 0.007395
shots = 10000


# %% Make a circuit
def fulladder(circuit, in1, in2, in3, carry):
    """in1, in2, in3 are the input qubits, carry is the output qubit,!!no sum"""
    circuit.ccx(in1, in2, carry)
    circuit.cx(in1, in2)
    circuit.ccx(in2, in3, carry)
    circuit.cx(in1, in2)


def testcircle(numofqubit, totalxtime, coorrate, makeerror):
    counts = shots % numofqubit
    for _ in range(shots // numofqubit):
        circ = boolcirc(numofqubit + 1, prob_2)
        for k in range(totalxtime):
            if makeerror > 0:
                for i in range(numofqubit):
                    circ.checkerror(i, makeerror)
            if k % coorrate == coorrate - 1:
                for i in range(numofqubit):
                    fulladder(
                        circ, (i - 1) % numofqubit, i, (i + 1) % numofqubit, numofqubit
                    )
                    circ.reset(i)
                    circ.cx(numofqubit, i)
                    circ.reset(numofqubit)
        counts += circ.count(0, numofqubit, False)
    return counts / shots


def testcircle_rand(numofqubit, totalxtime, coorrate, makeerror):
    counts = shots % numofqubit
    for _ in range(shots // numofqubit):
        circ = boolcirc(numofqubit + 1, prob_2)
        count = 0
        for k in range(totalxtime):
            if makeerror > 0:
                for i in range(numofqubit):
                    circ.checkerror(i, makeerror)
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
                for i in range(0, numofqubit, 2):
                    circ.swap(i, (i + 1) % numofqubit)
                for i in range(1, numofqubit, 2):
                    circ.swap(i, (i + 1) % numofqubit)
                count += 1
        counts += circ.count(0, numofqubit, False)
    return counts / shots


# %%
corrrate = 1  # 200
measurerate = 10  # 200
makeerror = 3
totaltime = 100  # 2000
x = range(0, totaltime, measurerate)

print("3 bit")
y1 = []
for i in x:
    y1.append(testcircle(3, i, corrrate, makeerror))
plt.plot(x, y1, color="r", label="corr")
for i in y1:
    print(i)

print("6 bit")
y1 = []
for i in x:
    y1.append(testcircle(10, i, corrrate, makeerror))
plt.plot(x, y1, color="g", label="corr")
for i in y1:
    print(i)


print("10 bit rand")
y1 = []
for i in x:
    y1.append(testcircle_rand(10, i, corrrate, makeerror))
    print(y1[-1])
plt.plot(x, y1, color="c", label="corr")

print("base")
y2 = []
for i in x:
    y2.append(testcircle(3, i, 1000000, makeerror))
for i in y2:
    print(i)


plt.plot(x, y2, color="k", label="no corr")
plt.title(f"correct per {corrrate} x gates prob_2={prob_2}")  # title
plt.ylabel("correct rate")  # y label
plt.xlabel("x gates")  # x label

plt.show()


# %%
