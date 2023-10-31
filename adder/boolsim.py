# %%
import numpy as np
from qiskit.visualization import plot_histogram


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

    def x(self, a):
        self.qubit[a] = not self.qubit[a]

    def cx(self, a, b):
        if self.qubit[a]:
            self.qubit[b] = not self.qubit[b]
        self.checkerror_ecr(a, b)

    def ccx(self, c1, c2, t):
        beginstate = self.qubit[c1] ^ self.qubit[c2]

        circ.checkerror_ecr(c1, t)
        circ.checkerror_ecr(c2, t)
        circ.checkerror_ecr(c1, t)
        circ.checkerror_ecr(c2, t)

        if self.qubit[c1] and self.qubit[c2]:
            self.qubit[t] = not self.qubit[t]

        self.qubit[t] ^= beginstate ^ self.qubit[c1] ^ self.qubit[c2]

        pass

    def __str__(self):
        s = ""
        for i in self.qubit:
            if i:
                s += "1"
            else:
                s += "0"
        return s


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


# %%
