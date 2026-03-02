# %%
import numpy as np

# %%
dtype = np.bool_
datasize = 60  # qubit size
initialdata = np.array([True] * datasize, dtype=dtype)
totalmeasuretime = 12000  # 要測量的次數
totaltime = 100  # 要糾錯(製造錯誤)的次數
errorrate = 0.00  # 錯誤率

prob_1 = 0.00021932  # 1-qubit gate 0.0002193
prob_2 = 0.007395  # 2-qubit gate 0.007395


def makeerror(data, errorr=errorrate):
    for i in range(datasize):
        if np.random.rand() < errorr:
            data[i] = not data[i]
    return data


def adderans(data, indexarr):
    newdata = makeerror(data, ((prob_1 * 9 + prob_2 * 6) * 2 + prob_2 * 2) / 3)
    newdata = np.array(
        [
            [
                newdata[(i + indexarr[0]) % datasize],
                newdata[(i + indexarr[1]) % datasize],
                newdata[(i + indexarr[2]) % datasize],
            ].count(True)
            >= 2
            for i in range(datasize)
        ],
        dtype=dtype,
    )
    newdata = makeerror(newdata, (prob_2 * 2))
    return newdata


# %% do nothing
correctcount = 0
for _ in range(totalmeasuretime // datasize):
    data = np.array(initialdata)
    for __ in range(totaltime):
        data = makeerror(data)
    correctcount += np.sum(data == True)
print(f"do nothing-> correct rate={correctcount/totalmeasuretime}")


# %% 3bit adder's carry
correctcount = 0
for _ in range(totalmeasuretime // datasize):
    data = np.array(initialdata)
    for __ in range(totaltime):
        data = makeerror(data)
        data = adderans(data, [-1, 0, 1])
    correctcount += np.sum(data == True)
print(f"3bit adder's carry-> correct rate={correctcount/totalmeasuretime}")

# %% 3bit adder's carry -1,0,2
correctcount = 0
for _ in range(totalmeasuretime // datasize):
    data = np.array(initialdata)
    for __ in range(totaltime):
        data = makeerror(data)
        data = adderans(data, [-1, 0, 2])
    correctcount += np.sum(data == True)
print(f"3bit adder's carry (-1,0,2) -> correct rate={correctcount/totalmeasuretime}")

# %% 3bit adder's carry (-1,0,2),(-2,0,1)
correctcount = 0
for _ in range(totalmeasuretime // datasize):
    data = np.array(initialdata)
    for __ in range(totaltime // 2):
        data = makeerror(data)
        data = adderans(data, [-1, 0, 2])
        data = makeerror(data)
        data = adderans(data, [-2, 0, 1])
    correctcount += np.sum(data == True)
print(
    f"3bit adder's carry (-1,0,2),(-2,0,1)-> correct rate={correctcount/totalmeasuretime}"
)

# %% 3bit adder's carry (-1,0,2),(-2,0,1) with circle swap
correctcount = 0
for _ in range(totalmeasuretime // datasize):
    data = np.array(initialdata)
    data = makeerror(data,0.36)
    for __ in range(totaltime // 2):
        data = makeerror(data)
        data = adderans(data, [-1, 0, 2])
        for i in range(0, datasize, 2):
            data[i], data[i + 1] = data[i + 1], data[i]
        for i in range(1, datasize, 2):
            data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]
        makeerror(data, prob_2 * 6)
        data = makeerror(data)
        data = adderans(data, [-2, 0, 1])
        for i in range(0, datasize, 2):
            data[i], data[i + 1] = data[i + 1], data[i]
        for i in range(1, datasize, 2):
            data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]
        makeerror(data, prob_2 * 6)
    correctcount += np.sum(data == True)
print(
    f"3bit adder's carry (-1,0,2),(-2,0,1) with circle swap-> correct rate={correctcount/totalmeasuretime}"
)


# %% 3bit adder's carry (-1,0,2) with circle swap
correctcount = 0
for _ in range(totalmeasuretime // datasize):
    data = np.array(initialdata)
    for __ in range(totaltime):
        data = makeerror(data)
        data = adderans(data, [-1, 0, 2])
        for i in range(0, datasize, 2):
            data[i], data[i + 1] = data[i + 1], data[i]
        for i in range(1, datasize, 2):
            data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]
        makeerror(data, prob_2 * 6)

    correctcount += np.sum(data == True)
print(
    f"3bit adder's carry (-1,0,2) with circle swap-> correct rate={correctcount/totalmeasuretime}"
)

# %% 3bit adder's carry with circle swap
correctcount = 0
for _ in range(totalmeasuretime // datasize):
    data = np.array(initialdata)
    for __ in range(totaltime // 2):
        data = makeerror(data)
        data = adderans(data, [-1, 0, 1])
        for i in range(0, datasize, 2):
            data[i], data[i + 1] = data[i + 1], data[i]
        for i in range(1, datasize, 2):
            data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]
        makeerror(data, prob_2 * 6)

        data = makeerror(data)
        data = adderans(data, [-1, 0, 1])
        for i in range(0, datasize, 2):
            data[i], data[i + 1] = data[i + 1], data[i]
        for i in range(1, datasize, 2):
            data[i], data[(i + 1) % datasize] = data[(i + 1) % datasize], data[i]
        makeerror(data, prob_2 * 6)
    correctcount += np.sum(data == True)
print(
    f"3bit adder's carry with circle swap-> correct rate={correctcount/totalmeasuretime}"
)


# %%
