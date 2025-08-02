from typing import List
from qc_coder.gates import Instruction


class BaseTranslator:
    """
    Clase base para traductores específicos de framework.

    Un traductor recibe una lista de Instruction y genera
    un circuito específico de un framework cuántico.
    """
    def translate(self, instructions: List[Instruction]):
        """
        Traduce una secuencia de Instruction a un objeto circuito
        propio del framework.

        :param instructions: Lista de objetos Instruction.
        :return: Circuito específico del framework.
        """
        raise NotImplementedError("Subclasses must implement translate() method.")
