from typing import List
from .base import BaseTranslator
from qc_coder.gates import Instruction
import cirq


class CirqTranslator(BaseTranslator):
    """
    Translates a list of Instruction objects into a Cirq Circuit.

    The translator uses a linear layout of LineQubit instances and
    appends operations corresponding to the intermediate representation
    produced by the parser.
    """

    def __init__(self, num_qubits: int):
        # Create a linear array of qubits: q_0, q_1, ..., q_{num_qubits-1}
        self.qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
        self.circuit = cirq.Circuit()

    def translate(self, instructions: List[Instruction]):
        """
        Populate a Cirq Circuit from the given list of instructions.

        The circuit is reset on each call, so the translator instance
        can be reused for multiple translation runs.

        :param instructions: List of Instruction objects.
        :return: cirq.Circuit with the corresponding operations applied.
        """
        # Reset the circuit for each translation
        self.circuit = cirq.Circuit()

        for instr in instructions:
            name = instr.name.upper()
            target_index = instr.targets[0]
            qubit = self.qubits[target_index]

            # Single-qubit Clifford+T gates
            if name == 'X':
                self.circuit.append(cirq.X(qubit))
            elif name == 'Y':
                self.circuit.append(cirq.Y(qubit))
            elif name == 'Z':
                self.circuit.append(cirq.Z(qubit))
            elif name == 'H':
                self.circuit.append(cirq.H(qubit))
            elif name == 'S':
                self.circuit.append(cirq.S(qubit))
            elif name == 'T':
                self.circuit.append(cirq.T(qubit))

            # Two-qubit controlled gates
            elif name in ('CNOT', 'CX'):
                control_qubit = self.qubits[instr.controls[0]]
                self.circuit.append(cirq.CNOT(control_qubit, qubit))

            # Parameterized rotations
            elif name == 'RX':
                self.circuit.append(cirq.rx(instr.params[0]).on(qubit))
            elif name == 'RZ':
                self.circuit.append(cirq.rz(instr.params[0]).on(qubit))

            # --------------------------------------------------------
            # Measurement operation:
            # MEASURE q -> cirq.measure(qubit, key="m<q>")
            # --------------------------------------------------------
            elif name == 'MEASURE':
                self.circuit.append(
                    cirq.measure(qubit, key=f"m{target_index}")
                )

            else:
                raise ValueError(
                    f"Gate '{name}' is not supported by CirqTranslator."
                )

        return self.circuit
