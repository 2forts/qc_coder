import json
from qc_coder.interface import UnifiedInterface
from qc_coder.gates import Instruction


def load_decomposition_map(path: str):
    """
    Optional helper to load a JSON-based decomposition map and
    convert it into a dictionary of lists of Instruction objects.
    """
    with open(path, 'r') as f:
        data = json.load(f)

    decomposition_map = {}
    for gate, seq in data.items():
        instructions = []
        for instr in seq:
            instructions.append(
                Instruction(
                    name=instr['name'],
                    targets=instr.get('targets', []),
                    controls=instr.get('controls', []),
                    params=instr.get('params', []),
                )
            )
        decomposition_map[gate.upper()] = instructions
    return decomposition_map


if __name__ == '__main__':
    # Try to load an optional decomposition map (not needed for teleportation)
    try:
        decomposition_map = load_decomposition_map('config/decomposition_map.json')
    except FileNotFoundError:
        decomposition_map = {}

    # ---------------------------------------------------------------------
    # Quantum teleportation circuit in the QC_Coder DSL
    #
    # Qubit layout:
    #   q0: input state to be teleported (Alice)
    #   q1: Alice's half of the Bell pair
    #   q2: Bob's half of the Bell pair
    #
    # The following token sequence implements:
    #   1. Bell pair preparation on (q1, q2): H1, CNOT1-2
    #   2. Bell-basis measurement on (q0, q1): CNOT0-1, H0
    #   3. Measurements of q0 and q1: MEASURE0, MEASURE1
    #
    # Classical conditional corrections on q2 (X/Z based on the
    # measurement outcomes) are intentionally left to the host program,
    # keeping the DSL focused on the quantum circuit structure.
    # ---------------------------------------------------------------------
    teleportation_tokens = [
        'H1',
        'CNOT1-2',
        'CNOT0-1',
        'H0',
        'MEASURE0',
        'MEASURE1',
    ]

    num_qubits = 3

    # ------------------------------------------------------------------
    # Qiskit backend
    # ------------------------------------------------------------------
    ui_qiskit = UnifiedInterface(
        framework='qiskit',
        num_qubits=num_qubits,
        decomposition_map=decomposition_map,
    )
    circuit_qiskit = ui_qiskit.build_circuit(teleportation_tokens)
    print('Qiskit teleportation circuit:')
    print(circuit_qiskit)

    # ------------------------------------------------------------------
    # Cirq backend
    # ------------------------------------------------------------------
    ui_cirq = UnifiedInterface(
        framework='cirq',
        num_qubits=num_qubits,
        decomposition_map=decomposition_map,
    )
    circuit_cirq = ui_cirq.build_circuit(teleportation_tokens)
    print('\nCirq teleportation circuit:')
    print(circuit_cirq)

    # ------------------------------------------------------------------
    # Amazon Braket backend
    # ------------------------------------------------------------------
    ui_braket = UnifiedInterface(
        framework='braket',
        num_qubits=num_qubits,
        decomposition_map=decomposition_map,
    )
    circuit_braket = ui_braket.build_circuit(teleportation_tokens)
    print('\nBraket teleportation circuit:')
    print(circuit_braket)
