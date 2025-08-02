from typing import List
from .base import BaseTranslator
from qc_coder.gates import Instruction

class QiskitTranslator(BaseTranslator):
    """
    Traduce una lista de Instruction a un QuantumCircuit de Qiskit.
    """
    def __init__(self, num_qubits: int):
        try:
            from qiskit import QuantumCircuit
n        except ImportError:
            raise ImportError("Para usar QiskitTranslator, instala qiskit con 'pip install qiskit'.")
        self.circuit = QuantumCircuit(num_qubits)

    def translate(self, instructions: List[Instruction]):
        """
        Añade puertas al QuantumCircuit según las instrucciones.

        :param instructions: Lista de objetos Instruction.
        :return: QuantumCircuit con las puertas aplicadas.
        """
        for instr in instructions:
            name = instr.name.upper()
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
            elif name in ('CNOT', 'CX'):
                self.circuit.cx(instr.controls[0], instr.targets[0])
            elif name == 'RX':
                self.circuit.rx(instr.params[0], instr.targets[0])
            elif name == 'RZ':
                self.circuit.rz(instr.params[0], instr.targets[0])
            else:
                # Pausar para permitir futuras extensiones
                raise ValueError(f"Puerta '{name}' no soportada por QiskitTranslator.")
        return self.circuit
