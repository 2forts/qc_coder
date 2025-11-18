import time
import random
import statistics

from qc_coder.interface import UnifiedInterface
from qc_coder.parser import Parser

# Backends available
BACKENDS = ["qiskit", "cirq", "braket"]

# Gate set restricted to what the parser directly supports (Clifford+T + CNOT)
ONE_QUBIT_GATES = ["H", "X", "Y", "Z", "S", "T"]
TWO_QUBIT_GATES = ["CNOT"]


def random_gate(num_qubits=5):
    """Generate a random valid QC_Coder token compatible with the current parser."""
    g = random.choice(ONE_QUBIT_GATES + TWO_QUBIT_GATES)
    if g in ONE_QUBIT_GATES:
        q = random.randint(0, num_qubits - 1)
        return f"{g}{q}"
    else:
        # CNOT q1-q2 with q1 != q2
        q1 = random.randint(0, num_qubits - 1)
        q2 = random.randint(0, num_qubits - 1)
        while q2 == q1:
            q2 = random.randint(0, num_qubits - 1)
        return f"CNOT{q1}-{q2}"


def generate_random_token_list(n, num_qubits=5):
    return [random_gate(num_qubits=num_qubits) for _ in range(n)]


def measure_translation_time(tokens, num_qubits=5, repeats=5):
    """
    Measure average parse time (tokens -> IR) and translation time
    (IR -> backend circuit) over a few repeats.
    """
    parser = Parser()
    parse_times = []
    backend_times = {b: [] for b in BACKENDS}

    for _ in range(repeats):
        # 1) parse timing
        t0 = time.perf_counter()
        ir = parser.parse_tokens(tokens)
        t1 = time.perf_counter()
        parse_times.append(t1 - t0)

        # 2) translation timing
        for backend in BACKENDS:
            ui = UnifiedInterface(framework=backend, num_qubits=num_qubits)
            t0 = time.perf_counter()
            _ = ui.build_circuit(tokens)
            t1 = time.perf_counter()
            backend_times[backend].append(t1 - t0)

    return (
        statistics.mean(parse_times),
        {b: statistics.mean(times) for b, times in backend_times.items()},
        ir,
    )


def get_gate_counts(ir):
    """Count 1-qubit, 2-qubit, and measurement operations from IR."""
    single = 0
    double = 0
    meas = 0
    for instr in ir:
        if instr.name == "MEASURE":
            meas += 1
        elif len(instr.controls) == 1:
            double += 1
        else:
            single += 1
    return single, double, meas


def get_qiskit_depth(ui, tokens):
    try:
        circ = ui.build_circuit(tokens)
        return circ.depth()
    except Exception:
        return None


def get_cirq_depth(ui, tokens):
    try:
        circ = ui.build_circuit(tokens)
        return len(circ.moments)
    except Exception:
        return None


def run_benchmarks():
    print(
        "size,parse_time,qiskit_time,cirq_time,braket_time,"
        "single_gates,double_gates,measurements,qiskit_depth,cirq_depth"
    )

    circuit_sizes = [10, 50, 100, 200, 500]

    for size in circuit_sizes:
        tokens = generate_random_token_list(size)

        parse_time, backend_times, ir = measure_translation_time(tokens)

        # gate counts (IR-level)
        s, d, m = get_gate_counts(ir)

        # compute depths (only for Qiskit and Cirq)
        ui_qiskit = UnifiedInterface("qiskit", 5)
        ui_cirq = UnifiedInterface("cirq", 5)
        qiskit_depth = get_qiskit_depth(ui_qiskit, tokens)
        cirq_depth = get_cirq_depth(ui_cirq, tokens)

        print(
            f"{size},"
            f"{parse_time:.5f},"
            f"{backend_times['qiskit']:.5f},"
            f"{backend_times['cirq']:.5f},"
            f"{backend_times['braket']:.5f},"
            f"{s},{d},{m},"
            f"{qiskit_depth},{cirq_depth}"
        )


if __name__ == "__main__":
    run_benchmarks()
