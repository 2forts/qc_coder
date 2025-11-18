from typing import List
from .base import BaseTranslator
from qc_coder.gates import Instruction


class QiskitTranslator(BaseTranslator):
    """
    Translates a list of Instruction objects into a Qiskit QuantumCircuit.

    This translator constructs a circuit with one classical bit per qubit,
    allowing MEASURE instructions to be mapped directly onto measure(q, c)
    operations following Qiskit's standard convention.
    """

    def __init__(self, num_qubits: int):
        try:
            from qiskit import QuantumCircuit
        except ImportError:
            raise ImportError(
                "To use QiskitTranslator, install qiskit with 'pip install qiskit'."
            )

        # Create a circuit with 'num_qubits' quantum wires and the same
        # number of classical bits for measurement readout.
        self.circuit = QuantumCircuit(num_qubits, num_qubits)
        self.num_qubits = num_qubits

    def translate(self, instructions: List[Instruction]):
        """
        Append quantum operations to the QuantumCircuit according to the
        provided intermediate-representation instructions.

        :param instructions: List of Instruction objects produced by the parser.
        :return: A fully populated QuantumCircuit.
        """
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
                self.circuit.cx(instr.controls[0], instr.targets[0])

            # Parameterized rotations (if present in the IR)
            elif name == 'RX':
                self.circuit.rx(instr.params[0], instr.targets[0])
            elif name == 'RZ':
                self.circuit.rz(instr.params[0], instr.targets[0])

            # --------------------------------------------------------
            # Measurement operation:
            # MEASURE q → measure qubit q into classical bit q.
            # --------------------------------------------------------
            elif name == 'MEASURE':
                q = instr.targets[0]
                self.circuit.measure(q, q)

            else:
                # Stop execution to signal unsupported instructions
                raise ValueError(
                    f"Gate '{name}' is not supported by QiskitTranslator."
                )

        return self.circuit
