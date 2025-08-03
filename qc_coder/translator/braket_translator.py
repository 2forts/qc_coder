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
        # Reinicializa el circuito para cada llamada
        from braket.circuits import Circuit
        self.circuit = Circuit()
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
                # Braket cnot usa control y target en lista
                self.circuit.cnot(control=instr.controls[0], target=instr.targets[0])
            elif instr.name == 'RX':
                # qubit primero, luego ángulo
                self.circuit.rx(instr.targets[0], instr.params[0])
            elif name == 'RZ':
                self.circuit.rz(instr.targets[0], instr.params[0])
            else:
                raise ValueError(f"Puerta '{name}' no soportada por BraketTranslator.")
        return self.circuit
