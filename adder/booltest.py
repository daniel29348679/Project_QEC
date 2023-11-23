# %%
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from multiprocessing import Pool


class boolcirc:
    def __init__(self, qubit, errorrate):
        # self.qubit = np.array([False] * qubit, dtype=np.bool_)
        self.qubit = [False] * qubit
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

    def swap_direct(self, a, b):
        self.qubit[a], self.qubit[b] = self.qubit[b], self.qubit[a]

    def permutation(self, a, b):
        self.qubit[a:b] = np.random.permutation(self.qubit[a:b])

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


# %% Make a circuit
def fulladder(circuit, in1, in2, in3, carry):
    """in1, in2, in3 are the input qubits, carry is the output qubit,!!no sum"""
    circuit.ccx(in1, in2, carry)
    circuit.cx(in1, in2)
    circuit.ccx(in2, in3, carry)
    circuit.cx(in1, in2)


def testcircle(numofqubit, totaltime, coorrate, makeerror, measurerate, shots, prob_2):
    counts = [shots % numofqubit] * (totaltime // measurerate + 1)
    for _ in tqdm(range(shots // numofqubit)):
        circ = boolcirc(numofqubit + 1, prob_2)
        for k in range(totaltime + 1):
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
            if k % measurerate == 0:
                counts[k // measurerate] += circ.count(0, numofqubit, False)
    return [i / shots for i in counts]


def testcircle_rand(
    numofqubit, totaltime, coorrate, makeerror, measurerate, shots, prob_2
):
    counts = [shots % numofqubit] * (totaltime // measurerate + 1)
    for _ in tqdm(range(shots // numofqubit)):
        circ = boolcirc(numofqubit + 1, prob_2)
        count = 0
        for k in range(totaltime + 1):
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
            if k % measurerate == 0:
                counts[k // measurerate] += circ.count(0, numofqubit, False)
    return [i / shots for i in counts]


def testcircle_r_d(
    numofqubit, totaltime, coorrate, makeerror, measurerate, shots, prob_2
):
    counts = [shots % numofqubit] * (totaltime // measurerate + 1)
    for _ in tqdm(range(shots // numofqubit)):
        circ = boolcirc(numofqubit * 2, prob_2)
        count = 0
        for k in range(totaltime + 1):
            if makeerror > 0:
                for i in range(numofqubit):
                    circ.checkerror(i, makeerror)
            if k % coorrate == coorrate - 1:
                for i in range(numofqubit):
                    circ.reset(i + numofqubit)
                    fulladder(
                        circ,
                        (i - 1 - count % 2) % numofqubit,
                        i,
                        (i + 1 + (count + 1) % 2) % numofqubit,
                        i + numofqubit,
                    )
                for i in range(0, numofqubit, 2):
                    circ.swap(i, (i + 1) % numofqubit)
                for i in range(1, numofqubit, 2):
                    circ.swap(i, (i + 1) % numofqubit)
            for i in range(numofqubit):
                circ.swap_direct(i + numofqubit, i)
            if k % measurerate == 0:
                counts[k // measurerate] += circ.count(0, numofqubit, False)
    return [i / shots for i in counts]


def testcircle_d_p(
    numofqubit, totaltime, coorrate, makeerror, measurerate, shots, prob_2
):
    counts = [shots % numofqubit] * (totaltime // measurerate + 1)
    for _ in tqdm(range(shots // numofqubit)):
        circ = boolcirc(numofqubit * 2, prob_2)
        for k in range(totaltime + 1):
            if makeerror > 0:
                for i in range(numofqubit):
                    circ.checkerror(i, makeerror)
            if k % coorrate == coorrate - 1:
                for i in range(numofqubit):
                    circ.reset(i + numofqubit)
                    fulladder(
                        circ,
                        (i - 1) % numofqubit,
                        i,
                        (i + 1) % numofqubit,
                        i + numofqubit,
                    )
            for i in range(numofqubit):
                circ.swap_direct(i + numofqubit, i)
            circ.permutation(0, numofqubit)
            if k % measurerate == 0:
                counts[k // measurerate] += circ.count(0, numofqubit, False)
    return [i / shots for i in counts]


def testcircle_R21(totaltime, makeerror, measurerate, shots, prob_2):
    """
     0  1  2  3  4  5  6  7  8
    19          20           9
    18 17 16 15 14 13 12 11 10
    """
    counts = [shots % 21] * (totaltime // measurerate + 1)
    for _ in tqdm(range(shots // 21)):
        circ = boolcirc(21 * 2, prob_2)
        for k in range(totaltime + 1):
            if makeerror > 0:
                for i in range(21):
                    circ.checkerror(i, makeerror)
            for i in range(10):
                circ.reset(i * 2 + 21)
                fulladder(
                    circ,
                    15,
                    16,
                    17,
                    i * 2 + 21,
                )
                circ.reset(i * 2 + 1 + 21)
                fulladder(
                    circ,
                    11,
                    12,
                    13,
                    i * 2 + 1 + 21,
                )
                for j in range(0, 20, 2):
                    circ.swap(j, j + 1)
                circ.swap(20, 14)
                for j in range(1, 20, 2):
                    circ.swap(j, (j + 1) % 20)
                circ.swap(20, 14)
            circ.reset(41)
            fulladder(
                circ,
                15,
                16,
                17,
                41,
            )

            for i in range(21):
                circ.swap_direct(i + 21, i)
            circ.permutation(0, 21)
            if k % measurerate == 0:
                counts[k // measurerate] += circ.count(0, 21, False)
    return [i / shots for i in counts]


def testcircle_R30(totaltime, makeerror, measurerate, shots, prob_2):
    """
     0  1  2  3  4  5  6  7  8  9 10 11 12
    27          28          29          13
    26 25 24 23 22 21 20 19 18 17 16 15 14
    """
    counts = [shots % 30] * (totaltime // measurerate + 1)
    for _ in tqdm(range(shots // 30)):
        circ = boolcirc(30 * 2, prob_2)
        for k in range(totaltime + 1):
            if makeerror > 0:
                for i in range(30):
                    circ.checkerror(i, makeerror)
            for i in range(10):
                circ.reset(i * 3 + 30)
                fulladder(
                    circ,
                    15,
                    16,
                    17,
                    i * 3 + 30,
                )
                circ.reset(i * 3 + 1 + 30)
                fulladder(
                    circ,
                    19,
                    20,
                    21,
                    i * 3 + 1 + 30,
                )
                circ.reset(i * 3 + 2 + 30)
                fulladder(
                    circ,
                    23,
                    24,
                    25,
                    i * 3 + 2 + 30,
                )
                for j in range(0, 28, 2):
                    circ.swap(j, j + 1)
                circ.swap(28, 22)
                circ.swap(29, 8)
                for j in range(1, 28, 2):
                    circ.swap(j, (j + 1) % 28)
                circ.swap(28, 22)
                circ.swap(29, 8)
            for i in range(30):
                circ.swap_direct(i + 30, i)
            # circ.permutation(0, 30)
            if k % measurerate == 0:
                counts[k // measurerate] += circ.count(0, 30, False)
    return [i / shots for i in counts]


# %%
if __name__ == "__main__":
    prob_2 = 0.002  # 2-qubit gate 0.007395 0.002795 0.001433
    shots = 10000
    corrrate = 1  # 200
    measurerate = 5  # 200
    makeerror = 5
    totaltime = 1000  # 2000
    x = range(0, totaltime + 1, measurerate)
    allsim = {}

    with Pool(19) as p:
        allsim["10bit_rand"] = p.apply_async(
            testcircle_rand,
            (10, totaltime, corrrate, makeerror, measurerate, shots, prob_2),
        )
        allsim["20bit_rand"] = p.apply_async(
            testcircle_rand,
            (20, totaltime, corrrate, makeerror, measurerate, shots, prob_2),
        )

        allsim["10bit_rand_d"] = p.apply_async(
            testcircle_r_d,
            (10, totaltime, corrrate, makeerror, measurerate, shots, prob_2),
        )
        allsim["20bit_rand_d"] = p.apply_async(
            testcircle_r_d,
            (20, totaltime, corrrate, makeerror, measurerate, shots, prob_2),
        )
        allsim["10bit_d_p"] = p.apply_async(
            testcircle_d_p,
            (10, totaltime, corrrate, makeerror, measurerate, shots, prob_2),
        )
        allsim["20bit_d_p"] = p.apply_async(
            testcircle_d_p,
            (20, totaltime, corrrate, makeerror, measurerate, shots, prob_2),
        )
        allsim["40bit_d_p"] = p.apply_async(
            testcircle_d_p,
            (40, totaltime, corrrate, makeerror, measurerate, shots, prob_2),
        )
        allsim["21bit_R"] = p.apply_async(
            testcircle_R21, (totaltime, makeerror, measurerate, shots, prob_2)
        )

        allsim["30bit_R"] = p.apply_async(
            testcircle_R30, (totaltime, makeerror, measurerate, shots, prob_2)
        )

        allsim["base"] = p.apply_async(
            testcircle, (6, totaltime, corrrate, makeerror, measurerate, shots, prob_2)
        )

        p.close()
        p.join()
        for i in allsim:
            allsim[i] = allsim[i].get()

    fig = plt.figure()
    fig.set_size_inches(16, 9)
    plt.plot(x, allsim["10bit_rand"], color="c", label="10 r")
    plt.plot(x, allsim["20bit_rand"], color="c", label="20 r")
    plt.plot(x, allsim["10bit_rand_d"], color="m", label="10 rd")
    plt.plot(x, allsim["20bit_rand_d"], color="m", label="20 rd")
    plt.plot(x, allsim["10bit_d_p"], color="gray", label="10 dp")
    plt.plot(x, allsim["20bit_d_p"], color="gray", label="20 dp")
    plt.plot(x, allsim["40bit_d_p"], color="gray", label="40 dp")
    plt.plot(x, allsim["21bit_R"], color="gold", label="21 R")
    plt.plot(x, allsim["30bit_R"], color="gold", label="30 R")
    print(allsim["21bit_R"])
    print(allsim["30bit_R"])

    plt.plot(x, allsim["base"], color="g", label="no corr")

    plt.title(f"correct per {makeerror} x gates prob_2={prob_2}")  # title
    plt.ylabel("correct rate")  # y label
    plt.xlabel(f"{makeerror}x CX gates")  # x label
    plt.legend()  # show legend

    # %%
