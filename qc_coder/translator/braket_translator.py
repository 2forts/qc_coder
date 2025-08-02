from typing import List
from .base import BaseTranslator
from qc_coder.gates import Instruction

try:
    from braket.circuits import Circuit
except ImportError:
    raise ImportError("Para usar BraketTranslator, instala amazon-braket-sdk con 'pip install amazon-braket-sdk'.")

class BraketTranslator(BaseTranslator):
    """
    Traduce una lista de Instruction a un Circuit de Amazon Braket.
    """
    def __init__(self, num_qubits: int):
        self.circuit = Circuit()
        self.num_qubits = num_qubits

    def translate(self, instructions: List[Instruction]):
        """
        Añade operaciones al Circuit de Braket según las instrucciones.

        :param instructions: Lista de objetos Instruction.
        :return: braket.circuits.Circuit con las puertas aplicadas.
        """
        for instr in instructions:
            name = instr.name.upper()
            if name == 'X':
                self.circuit.x(targets=instr.targets)
            elif name == 'Y':
                self.circuit.y(targets=instr.targets)
            elif name == 'Z':
                self.circuit.z(targets=instr.targets)
            elif name == 'H':
                self.circuit.h(targets=instr.targets)
            elif name == 'S':
                self.circuit.s(targets=instr.targets)
            elif name == 'T':
                self.circuit.t(targets=instr.targets)
            elif name in ('CNOT', 'CX'):
                # Braket cnot usa control y target en lista
                self.circuit.cnot(control=instr.controls[0], target=instr.targets[0])
            elif name == 'RX':
                self.circuit.rx(angle=instr.params[0], targets=instr.targets)
            elif name == 'RZ':
                self.circuit.rz(angle=instr.params[0], targets=instr.targets)
            else:
                raise ValueError(f"Puerta '{name}' no soportada por BraketTranslator.")
        return self.circuit
