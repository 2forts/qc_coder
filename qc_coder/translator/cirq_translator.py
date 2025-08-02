from typing import List
from .base import BaseTranslator
from qc_coder.gates import Instruction
import cirq

class CirqTranslator(BaseTranslator):
    """
    Traduce una lista de Instruction a un Circuit de Cirq.
    """
    def __init__(self, num_qubits: int):
        # Crear qubits lineales
        self.qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
        self.circuit = cirq.Circuit()

    def translate(self, instructions: List[Instruction]):
        """
        Añade operaciones al Circuit según las instrucciones.

        :param instructions: Lista de objetos Instruction.
        :return: cirq.Circuit con las puertas aplicadas.
        """
        for instr in instructions:
            name = instr.name.upper()
            if name == 'X':
                self.circuit.append(cirq.X(self.qubits[instr.targets[0]]))
            elif name == 'Y':
                self.circuit.append(cirq.Y(self.qubits[instr.targets[0]]))
            elif name == 'Z':
                self.circuit.append(cirq.Z(self.qubits[instr.targets[0]]))
            elif name == 'H':
                self.circuit.append(cirq.H(self.qubits[instr.targets[0]]))
            elif name == 'S':
                self.circuit.append(cirq.S(self.qubits[instr.targets[0]]))
            elif name == 'T':
                self.circuit.append(cirq.T(self.qubits[instr.targets[0]]))
            elif name in ('CNOT', 'CX'):
                self.circuit.append(cirq.CNOT(self.qubits[instr.controls[0]], self.qubits[instr.targets[0]]))
            elif name == 'RX':
                self.circuit.append(cirq.rx(instr.params[0])(self.qubits[instr.targets[0]]))
            elif name == 'RZ':
                self.circuit.append(cirq.rz(instr.params[0])(self.qubits[instr.targets[0]]))
            else:
                raise ValueError(f"Puerta '{name}' no soportada por CirqTranslator.")
        return self.circuit
