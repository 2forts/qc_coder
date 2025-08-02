import json
from qc_coder.interface import UnifiedInterface
from qc_coder.gates import Instruction


def load_decomposition_map(path: str):
    with open(path, 'r') as f:
        data = json.load(f)
    # Convert dict of dicts to dict of List[Instruction]
    decomposition_map = {}
    for gate, seq in data.items():
        instructions = []
        for instr in seq:
            instructions.append(
                Instruction(
                    name=instr['name'],
                    targets=instr.get('targets', []),
                    controls=instr.get('controls', []),
                    params=instr.get('params', [])
                )
            )
        decomposition_map[gate.upper()] = instructions
    return decomposition_map


if __name__ == '__main__':
    # Carga un mapa de descomposición opcional
    try:
        decomposition_map = load_decomposition_map('config/decomposition_map.json')
    except FileNotFoundError:
        decomposition_map = {}

    # Inicia la interfaz para Qiskit con 5 qubits
    ui_qiskit = UnifiedInterface(
        framework='qiskit',
        num_qubits=5,
        decomposition_map=decomposition_map
    )
    tokens = ['H0', 'CNOT0-1', 'T1', 'X2', 'MYGATE3']
    circuit_qiskit = ui_qiskit.build_circuit(tokens)
    print('Qiskit circuit:')
    print(circuit_qiskit)

    # Inicia la interfaz para Cirq
    ui_cirq = UnifiedInterface(
        framework='cirq',
        num_qubits=5,
        decomposition_map=decomposition_map
    )
    circuit_cirq = ui_cirq.build_circuit(tokens)
    print('\nCirq circuit:')
    print(circuit_cirq)

    # Inicia la interfaz para Amazon Braket
    ui_braket = UnifiedInterface(
        framework='braket',
        num_qubits=5,
        decomposition_map=decomposition_map
    )
    circuit_braket = ui_braket.build_circuit(tokens)
    print('\nBraket circuit:')
    print(circuit_braket)
