# %%
import numpy as np

# %%
dtype = np.float64
datasize = 20
initialdata = np.array([abs(i - datasize / 2) for i in range(datasize)], dtype=dtype)

totaltime = 20
# %%
print(f"initialdata's sd={np.std(initialdata)}")

# %% 3bit adder's carry
data = np.array(initialdata)
for _ in range(totaltime):
    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 1) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata
print(f"3bit adder's carry-> sd={np.std(data)}")
# %% 3bit adder's carry -1,0,2
data = np.array(initialdata)
for _ in range(totaltime):
    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 2) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata
print(f"3bit adder's carry -1,0,2-> sd={np.std(data)}")
# %% 3bit adder's carry (-1,0,2),(-2,0,1)
data = np.array(initialdata)
for _ in range(totaltime // 2):
    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 2) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata
    newdata = np.array(
        [
            (data[i - 2] + data[i] + data[(i + 1) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata
print(f"3bit adder's carry (-1,0,2),(-2,0,1)-> sd={np.std(data)}")

# %% 3bit adder's carry (-1,0,2),(-2,0,1) with circle swap
data = np.array(initialdata)
for _ in range(totaltime // 2):
    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 2) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata

    for i in range(0, datasize, 2):
        data[i], data[i + 1] = data[i + 1], data[i]

    newdata = np.array(
        [
            (data[i - 2] + data[i] + data[(i + 1) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata

    for i in range(1, datasize, 2):
        data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]

print(f"3bit adder's carry (-1,0,2),(-2,0,1) with circle swap-> sd={np.std(data)}")
# %% 3bit adder's carry (-1,0,2) with circle swap
data = np.array(initialdata)
for _ in range(totaltime // 2):
    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 2) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata

    for i in range(0, datasize, 2):
        data[i], data[i + 1] = data[i + 1], data[i]

    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 2) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata

    for i in range(1, datasize, 2):
        data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]

print(f"3bit adder's carry (-1,0,2) with circle swap-> sd={np.std(data)}")
# %% 3bit adder's carry with circle swap
data = np.array(initialdata)
for _ in range(totaltime // 2):
    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 1) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata

    for i in range(0, datasize, 2):
        data[i], data[i + 1] = data[i + 1], data[i]

    newdata = np.array(
        [
            (data[i - 1] + data[i] + data[(i + 1) % datasize]) / 3
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    data = newdata

    for i in range(1, datasize, 2):
        data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]

print(f"3bit adder's carry with circle swap-> sd={np.std(data)}")

# %%
