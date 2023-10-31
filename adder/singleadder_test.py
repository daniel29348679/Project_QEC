# %%
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import qiskit.providers.aer.noise as noise
import matplotlib.pyplot as plt

# Error probabilities (from ibm_sherbrooke)
prob_1 = 0.000  # 1-qubit gate 0.0002193
prob_2 = 0.001  # 2-qubit gate 0.007395

error_1 = noise.depolarizing_error(prob_1, 1)
error_2 = noise.depolarizing_error(prob_2, 2)

noise_model = noise.NoiseModel()
noise_model.add_all_qubit_quantum_error(error_1, ["u1", "u2", "u3"])
noise_model.add_all_qubit_quantum_error(error_2, ["cx"])

basis_gates = noise_model.basis_gates

shots = 1000000


# %% Make a circuit
def fulladder(circuit, in1, in2, in3, carry):
    """in1, in2, in3 are the input qubits, carry is the output qubit,!!no sum"""
    circuit.ccx(in1, in2, carry)
    circuit.cx(in1, in2)
    circuit.ccx(in2, in3, carry)
    circuit.cx(in1, in2)


def testadder(initialstate):
    circ = QuantumCircuit(4, 3)
    circ.initialize(initialstate, [0, 1, 2])
    fulladder(circ, 0, 1, 2, 3)
    circ.reset(1)
    circ.cx(3, 1)
    circ.reset(3)

    circ.measure([0, 1, 2], [0, 1, 2])
    result = execute(
        circ,
        Aer.get_backend("qasm_simulator"),
        basis_gates=basis_gates,
        noise_model=noise_model,
        shots=shots,
    ).result()
    counts = result.get_counts(0)
    return counts


# %%
str = "110"
ans = testadder(str)
print(str)
print(f"單位={shots*prob_2}")
ans
# %%
