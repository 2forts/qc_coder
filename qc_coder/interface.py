from typing import List, Dict, Optional

from .parser import Parser
from .translator.qiskit_translator import QiskitTranslator
from .translator.cirq_translator import CirqTranslator
from .translator.braket_translator import BraketTranslator
from .gates import Instruction


class UnifiedInterface:
    """
    Interfaz unificada para parsing de tokens y generación de circuitos en diferentes frameworks.

    :param framework: Nombre del framework ('qiskit', 'cirq', 'braket').
    :param num_qubits: Número de qubits del circuito.
    :param decomposition_map: Mapa opcional de descomposición para puertas no Clifford+T.
    """
    def __init__(
        self,
        framework: str,
        num_qubits: int,
        decomposition_map: Optional[Dict[str, List[Instruction]]] = None
    ):
        self.parser = Parser(decomposition_map)
        self.num_qubits = num_qubits
        self.translator = self._get_translator(framework.lower())

    def _get_translator(self, framework: str):
        if framework == 'qiskit':
            return QiskitTranslator(self.num_qubits)
        elif framework == 'cirq':
            return CirqTranslator(self.num_qubits)
        elif framework == 'braket':
            return BraketTranslator(self.num_qubits)
        else:
            raise ValueError(f"Framework no soportado: {framework}. Elige 'qiskit', 'cirq' o 'braket'.")

    def build_circuit(self, tokens: List[str]):
        """
        Construye el circuito a partir de una lista de tokens simbólicos.

        :param tokens: Lista de strings tipo ['H0', 'CNOT0-1', 'T2', ...]
        :return: Circuito generado según el framework elegido.
        """
        # Parsear tokens a instrucciones
        instructions: List[Instruction] = self.parser.parse_tokens(tokens)
        # Traducir instrucciones a circuito framework-specific
        circuit = self.translator.translate(instructions)
        return circuit
