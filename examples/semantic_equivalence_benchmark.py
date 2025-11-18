import random
import statistics
from typing import List

import numpy as np

from qc_coder.interface import UnifiedInterface
from qc_coder.parser import Parser


# Gate set restricted to what the current parser supports natively (Clifford+T + CNOT)
ONE_QUBIT_GATES = ["H", "X", "Y", "Z", "S", "T"]
TWO_QUBIT_GATES = ["CNOT"]

CIRCUIT_SIZES = [10, 50, 100, 200, 500]
NUM_QUBITS = 5
CIRCUITS_PER_SIZE = 5  # number of random circuits per size


def random_gate(num_qubits: int) -> str:
    """
    Generate a random valid QC_Coder token for a unitary circuit
    using only Clifford+T and CNOT gates.
    """
    g = random.choice(ONE_QUBIT_GATES + TWO_QUBIT_GATES)
    if g in ONE_QUBIT_GATES:
        q = random.randint(0, num_qubits - 1)
        return f"{g}{q}"
    else:
        # CNOT with distinct control and target
        c = random.randint(0, num_qubits - 1)
        t = random.randint(0, num_qubits - 1)
        while t == c:
            t = random.randint(0, num_qubits - 1)
        return f"CNOT{c}-{t}"


def generate_random_tokens(n: int, num_qubits: int) -> List[str]:
    """
    Generate a list of n tokens, ensuring that all qubits are used
    at least once by prefixing the circuit with H gates on each qubit.
    """
    if n < num_qubits:
        raise ValueError("Circuit size must be at least the number of qubits.")

    # Prefix: ensure each qubit appears at least once
    tokens = [f"H{i}" for i in range(num_qubits)]

    # Remaining random gates
    remaining = n - num_qubits
    tokens.extend(random_gate(num_qubits) for _ in range(remaining))
    return tokens


def statevector_qiskit(tokens: List[str], num_qubits: int) -> np.ndarray:
    """
    Build a Qiskit circuit via QC_Coder and return the final statevector.
    Assumes a unitary circuit (no measurements).
    """
    from qiskit.quantum_info import Statevector

    ui = UnifiedInterface(framework="qiskit", num_qubits=num_qubits)
    qc = ui.build_circuit(tokens)
    sv = Statevector.from_instruction(qc)
    return np.array(sv.data, dtype=complex)


def statevector_cirq(tokens: List[str], num_qubits: int) -> np.ndarray:
    """
    Build a Cirq circuit via QC_Coder and return the final statevector.
    Assumes a unitary circuit (no measurements).
    """
    import cirq

    ui = UnifiedInterface(framework="cirq", num_qubits=num_qubits)
    circuit = ui.build_circuit(tokens)
    sim = cirq.Simulator()
    result = sim.simulate(circuit)
    sv = result.final_state_vector
    return np.array(sv, dtype=complex)


def fidelity(psi: np.ndarray, phi: np.ndarray) -> float:
    """
    Compute state fidelity |<psi|phi>|^2 between normalized statevectors.
    """
    psi_n = psi / np.linalg.norm(psi)
    phi_n = phi / np.linalg.norm(phi)
    overlap = np.vdot(psi_n, phi_n)
    return float(abs(overlap) ** 2)


def run_semantic_equivalence_benchmark():
    """
    For each circuit size, generate several random circuits, translate them
    to Qiskit and Cirq via QC_Coder, and compare the resulting statevectors
    using fidelity. Print summary statistics in CSV format.
    """
    # Fix seed for reproducibility
    random.seed(42)

    print("size,num_circuits,min_fidelity,mean_fidelity,max_fidelity")

    parser = Parser()

    for size in CIRCUIT_SIZES:
        fidelities: List[float] = []

        for _ in range(CIRCUITS_PER_SIZE):
            tokens = generate_random_tokens(size, NUM_QUBITS)

            # Ensure tokens are parsable (this also stresses the parser)
            _ = parser.parse_tokens(tokens)

            # Compute final statevectors for Qiskit and Cirq
            psi_qiskit = statevector_qiskit(tokens, NUM_QUBITS)
            psi_cirq = statevector_cirq(tokens, NUM_QUBITS)

            fid = fidelity(psi_qiskit, psi_cirq)
            fidelities.append(fid)

        min_fid = min(fidelities)
        max_fid = max(fidelities)
        mean_fid = statistics.mean(fidelities)

        print(
            f"{size},{CIRCUITS_PER_SIZE},"
            f"{min_fid:.10f},{mean_fid:.10f},{max_fid:.10f}"
        )


if __name__ == "__main__":
    run_semantic_equivalence_benchmark()
