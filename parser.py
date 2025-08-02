import re
from typing import List, Dict, Optional

from .gates import Instruction


class Parser:
    """
    Parser de instrucciones simbólicas de puertas cuánticas.

    Convierte tokens tipo "X2", "CNOT1-3" en objetos Instruction.
    Soporta puertas Clifford+T por defecto; para puertas custom fuera de Clifford+T,
    utiliza un mapa de descomposición proporcionado.
    """
    # Expresión regular para nombres y qubits (e.g., 'H0', 'CNOT1-3')
    TOKEN_REGEX = re.compile(r'^(?P<name>[A-Za-z]+)(?P<qubits>\d+(-\d+)*)$')

    def __init__(self, decomposition_map: Optional[Dict[str, List[Instruction]]] = None):
        """
        :param decomposition_map: Mapa de descomposición para puertas no Clifford+T.
                                  Clave: nombre de la puerta, Valor: lista de Instruction.
        """
        self.decomposition_map = decomposition_map or {}

    def parse(self, token: str) -> List[Instruction]:
        """
        Parsea un token simple en una o varias instrucciones.

        :param token: String con formato 'GATE{n}' o 'GATE{c}-{t}'.
        :return: Lista de objetos Instruction.
        :raises ValueError: Si el token no coincide o falta descomposición.
        """
        match = self.TOKEN_REGEX.match(token)
        if not match:
            raise ValueError(f"Token '{token}' no coincide con el formato esperado.")

        name = match.group('name').upper()
        qubits_str = match.group('qubits')
        parts = qubits_str.split('-')

        # Un solo qubit: puerta de un solo qubit
        if len(parts) == 1:
            target = int(parts[0])
            instr = Instruction(name=name, targets=[target], controls=[])
            instructions = [instr]
        # Dos qubits: control-target
        elif len(parts) == 2:
            control, target = map(int, parts)
            # Normalizar nombre para CNOT
            gate_name = 'CNOT' if name in ('CNOT', 'CX') else name
            instr = Instruction(name=gate_name, targets=[target], controls=[control])
            instructions = [instr]
        else:
            raise ValueError(f"Token '{token}' tiene formato inválido con múltiples '-'.")

        # Descomponer puertas no Clifford+T
        if name not in {'X', 'Y', 'Z', 'H', 'S', 'T', 'CNOT', 'CX'}:
            if name in self.decomposition_map:
                return self.decomposition_map[name]
            else:
                raise ValueError(f"Puerta '{name}' no es Clifford+T y no tiene descomposición en el mapa.")

        return instructions

    def parse_tokens(self, tokens: List[str]) -> List[Instruction]:
        """
        Parsea una lista de tokens en secuencia de instrucciones.

        :param tokens: Lista de strings de instrucciones.
        :return: Lista de objetos Instruction.
        """
        all_instrs: List[Instruction] = []
        for tok in tokens:
            all_instrs.extend(self.parse(tok))
        return all_instrs
