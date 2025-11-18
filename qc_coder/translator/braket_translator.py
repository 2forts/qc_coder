from typing import List
from .base import BaseTranslator
from qc_coder.gates import Instruction

try:
    from braket.circuits import Circuit
except ImportError:
    raise ImportError(
        "To use BraketTranslator, install amazon-braket-sdk with "
        "'pip install amazon-braket-sdk'."
    )


class BraketTranslator(BaseTranslator):
    """
    Translates a list of Instruction objects into an Amazon Braket Circuit.

    The translator reconstructs a fresh Circuit on each call, ensuring
    that the same instance can be reused without preserving state between
    independent translation runs.
    """

    def __init__(self, num_qubits: int):
        self.circuit = Circuit()
        self.num_qubits = num_qubits

    def translate(self, instructions: List[Instruction]):
        """
        Append operations to the Braket Circuit according to the provided
        intermediate-representation instructions.

        :param instructions: List of Instruction objects.
        :return: braket.circuits.Circuit containing the applied operations.
        """
        # Reset the circuit for each translation call
        from braket.circuits import Circuit
        self.circuit = Circuit()

        for instr in instructions:
            name = instr.name.upper()

            # Single-qubit Clifford+T gates
            if name == 'X':
                self.circuit.x(instr.targets[0])
            elif name == 'Y':
                self.circuit.y(instr.targets[0])
            elif name == 'Z':
                self.circuit.z(instr.targets[0])
            elif name == 'H':
                self.circuit.h(instr.targets[0])
            elif name == 'S':
                self.circuit.s(instr.targets[0])
            elif name == 'T':
                self.circuit.t(instr.targets[0])

            # Controlled operations
            elif name in ('CNOT', 'CX'):
                # Braket requires explicit control and target parameters
                self.circuit.cnot(
                    control=instr.controls[0],
                    target=instr.targets[0]
                )

            # Parameterized rotations
            elif name == 'RX':
                # Braket rotation signature: rx(qubit, angle)
                self.circuit.rx(instr.targets[0], instr.params[0])
            elif name == 'RZ':
                self.circuit.rz(instr.targets[0], instr.params[0])

            # --------------------------------------------------------
            # Measurement operation:
            # MEASURE q -> circuit.measure(q)
            # Braket does not require explicit classical registers;
            # results are recorded based on qubit indices.
            # --------------------------------------------------------
            elif name == 'MEASURE':
                target = instr.targets[0]
                self.circuit.measure(target)

            else:
                raise ValueError(
                    f"Gate '{name}' is not supported by BraketTranslator."
                )

        return self.circuit
