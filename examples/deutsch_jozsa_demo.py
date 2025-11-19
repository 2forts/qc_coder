import json
from qc_coder.interface import UnifiedInterface
from qc_coder.gates import Instruction


def load_decomposition_map(path: str):
    """
    Optional helper to load a JSON-based decomposition map and
    convert it into a dictionary of lists of Instruction objects.
    """
    with open(path, "r") as f:
        data = json.load(f)

    decomposition_map = {}
    for gate, seq in data.items():
        instructions = []
        for instr in seq:
            instructions.append(
                Instruction(
                    name=instr["name"],
                    targets=instr.get("targets", []),
                    controls=instr.get("controls", []),
                    params=instr.get("params", []),
                )
            )
        decomposition_map[gate.upper()] = instructions
    return decomposition_map


if __name__ == "__main__":
    # --------------------------------------------------------------
    # Deutsch–Jozsa para N = 4 (2 qubits de entrada),
    # con un oracle balanceado f(x0, x1) = x0 XOR x1.
    #
    # Qubit layout:
    #   q0, q1 : qubits de entrada
    #   q2     : ancilla (inicializada a |1>)
    #
    # Pasos:
    #   1. Preparar |001> con X2.
    #   2. H en todos los qubits: H0, H1, H2.
    #   3. Oracle balanceado:
    #         CNOT0-2
    #         CNOT1-2
    #   4. H en qubits de entrada: H0, H1.
    #   5. Medir q0, q1.
    #
    # Si el resultado es distinto de 00, la función es balanceada.
    # --------------------------------------------------------------
    deutsch_jozsa_tokens = [
        # 1. Preparación del ancilla en |1>
        "X2",

        # 2. Hadamards iniciales
        "H0",
        "H1",
        "H2",

        # 3. Oracle balanceado f(x0, x1) = x0 XOR x1
        "CNOT0-2",
        "CNOT1-2",

        # 4. Hadamards finales sobre los qubits de entrada
        "H0",
        "H1",

        # 5. Medida de los qubits de entrada
        "MEASURE0",
        "MEASURE1",
    ]

    num_qubits = 3

    # Intentar cargar un decomposition_map (no necesario aquí, pero coherente
    # con el resto de ejemplos del repositorio)
    try:
        decomposition_map = load_decomposition_map("config/decomposition_map.json")
    except FileNotFoundError:
        decomposition_map = {}

    # --------------------------------------------------------------
    # Qiskit backend
    # --------------------------------------------------------------
    ui_qiskit = UnifiedInterface(
        framework="qiskit",
        num_qubits=num_qubits,
        decomposition_map=decomposition_map,
    )
    circuit_qiskit = ui_qiskit.build_circuit(deutsch_jozsa_tokens)
    print("Qiskit Deutsch–Jozsa circuit:")
    print(circuit_qiskit)

    # --------------------------------------------------------------
    # Cirq backend
    # --------------------------------------------------------------
    ui_cirq = UnifiedInterface(
        framework="cirq",
        num_qubits=num_qubits,
        decomposition_map=decomposition_map,
    )
    circuit_cirq = ui_cirq.build_circuit(deutsch_jozsa_tokens)
    print("\nCirq Deutsch–Jozsa circuit:")
    print(circuit_cirq)

    # --------------------------------------------------------------
    # Amazon Braket backend
    # --------------------------------------------------------------
    ui_braket = UnifiedInterface(
        framework="braket",
        num_qubits=num_qubits,
        decomposition_map=decomposition_map,
    )
    circuit_braket = ui_braket.build_circuit(deutsch_jozsa_tokens)
    print("\nBraket Deutsch–Jozsa circuit:")
    print(circuit_braket)
