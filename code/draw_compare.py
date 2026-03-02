from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import matplotlib.pyplot as plt

# ---------- shared building blocks ----------
def fulladder(circuit, a, b, c, carry):
    """carry ^= ab ^ ac ^ bc (majority carry), modifies b temporarily then restores"""
    circuit.ccx(a, b, carry)
    circuit.cx(a, b)
    circuit.ccx(b, c, carry)
    circuit.cx(a, b)

# ---------- 3-bit circuit (from 3bit_test.py) ----------
def corr_3bit(circuit):
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

def build_3bit(total_xtime=100, coorrate=100):
    circ = QuantumCircuit(9, 3)
    for k in range(total_xtime):
        circ.x([0, 1, 2])          # 你原程式每步都 X (固定翻轉，不是隨機錯誤)
        circ.barrier()
        if k % coorrate == coorrate - 1:
            corr_3bit(circ)
    circ.measure([0, 1, 2], [0, 1, 2])
    return circ

# ---------- 9-bit circuit (from 9bit.py) ----------
def corr_9bit(circuit):
    circuit.barrier()
    fulladder(circuit, 0, 1, 2, 9)
    fulladder(circuit, 3, 4, 5, 10)
    fulladder(circuit, 6, 7, 8, 11)

    # block A fixes q0..q2 using syndrome q9 via temp q12
    circuit.cx([0, 9], 12); circuit.cx(12, 0); circuit.reset(12)
    circuit.cx([1, 9], 12); circuit.cx(12, 1); circuit.reset(12)
    circuit.cx([2, 9], 12); circuit.cx(12, 2); circuit.reset(12)

    # block B fixes q3..q5 using syndrome q10 via temp q12
    circuit.cx([3, 10], 12); circuit.cx(12, 3); circuit.reset(12)
    circuit.cx([4, 10], 12); circuit.cx(12, 4); circuit.reset(12)
    circuit.cx([5, 10], 12); circuit.cx(12, 5); circuit.reset(12)

    # block C: 注意你原檔這裡回寫到 q3,q4,q5（不是 q6,q7,q8）
    circuit.cx([6, 11], 12); circuit.cx(12, 3); circuit.reset(12)
    circuit.cx([7, 11], 12); circuit.cx(12, 4); circuit.reset(12)
    circuit.cx([8, 11], 12); circuit.cx(12, 5); circuit.reset(12)

    circuit.reset([9, 10, 11])

def build_9bit(total_xtime=100, coorrate=100):
    circ = QuantumCircuit(13, 1)
    for k in range(total_xtime):
        circ.x(range(9))
        circ.barrier()
        if k % coorrate == coorrate - 1:
            corr_9bit(circ)
    circ.measure([0], [0])
    return circ

# ---------- draw helpers ----------
def save_circuit_png(circ, filename, title, fold=60):
    fig = circ.draw("mpl", fold=fold, idle_wires=False)
    fig.suptitle(title)
    fig.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close(fig)

def main():
    backend = Aer.get_backend("aer_simulator")

    # 你可以改這兩個參數來看「電路長度」差異
    total_xtime = 100
    coorrate = 100

    c3 = build_3bit(total_xtime=total_xtime, coorrate=coorrate)
    c9 = build_9bit(total_xtime=total_xtime, coorrate=coorrate)

    # Raw diagrams
    save_circuit_png(c3, "3bit_raw.png", f"3-bit raw (total_xtime={total_xtime}, coorrate={coorrate})")
    save_circuit_png(c9, "9bit_raw.png", f"9-bit raw (total_xtime={total_xtime}, coorrate={coorrate})")

    # Transpiled/expanded diagrams (this is the "gate expansion" you want)
    # 注意：transpile 後 ccx 會被拆成很多 cx + 單量子門
    t3 = transpile(c3, backend, optimization_level=0)
    t9 = transpile(c9, backend, optimization_level=0)

    print("3-bit transpiled ops:", t3.count_ops())
    print("9-bit transpiled ops:", t9.count_ops())

    save_circuit_png(t3, "3bit_transpiled.png", f"3-bit transpiled/expanded (ops shown in terminal)")
    save_circuit_png(t9, "9bit_transpiled.png", f"9-bit transpiled/expanded (ops shown in terminal)")

    print("Saved: 3bit_raw.png, 3bit_transpiled.png, 9bit_raw.png, 9bit_transpiled.png")

if __name__ == "__main__":
    main()