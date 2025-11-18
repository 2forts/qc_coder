import re
from typing import List, Dict, Optional

from .gates import Instruction


class Parser:
    """
    Parser for symbolic quantum gate instructions.

    Converts tokens such as "X2", "CNOT1-3", or "MEASURE0"
    into Instruction objects. Supports Clifford+T gates by
    default, and relies on a user-provided decomposition map
    for any unsupported custom gates.

    This parser operates at the DSL level and returns a backend-
    agnostic intermediate representation that will later be
    consumed by the framework-specific translators.
    """

    # Regular expression for tokens of the form NAME + qubit specification
    # Examples: "H0", "CNOT1-3", "RX2", "MEASURE0"
    TOKEN_REGEX = re.compile(r'^(?P<name>[A-Za-z]+)(?P<qubits>\d+(-\d+)*)$')

    def __init__(self, decomposition_map: Optional[Dict[str, List[Instruction]]] = None):
        """
        :param decomposition_map:
            Dictionary mapping custom gate names to a list of
            Instruction objects representing their decomposition
            into Clifford+T primitives.
        """
        self.decomposition_map = decomposition_map or {}

    def parse(self, token: str) -> List[Instruction]:
        """
        Parse a single DSL token into one or more Instruction objects.

        :param token: String of the form "GATE{n}" or "GATE{c}-{t}".
        :return: A list of Instruction objects.
        :raises ValueError: If the token is malformed or an unsupported
                            gate lacks a decomposition rule.
        """
        match = self.TOKEN_REGEX.match(token)
        if not match:
            raise ValueError(f"Token '{token}' does not match the expected format.")

        name = match.group('name').upper()
        qubits_str = match.group('qubits')
        parts = qubits_str.split('-')

        # --------------------------------------------------------
        # Special case: MEASURE operations (non-unitary)
        # --------------------------------------------------------
        # MEASURE tokens must specify exactly one qubit, e.g. MEASURE0.
        # Measurement is not part of the Clifford+T gate set and should
        # not be subject to decomposition. We therefore handle it directly
        # and return the corresponding Instruction immediately.
        # --------------------------------------------------------
        if name == 'MEASURE':
            if len(parts) != 1:
                raise ValueError(
                    f"Measurement token '{token}' must refer to exactly one qubit."
                )
            target = int(parts[0])
            instr = Instruction(name='MEASURE', targets=[target], controls=[])
            return [instr]

        # --------------------------------------------------------
        # Single-qubit gate: e.g. "H0", "X2"
        # --------------------------------------------------------
        if len(parts) == 1:
            target = int(parts[0])
            instr = Instruction(name=name, targets=[target], controls=[])
            instructions = [instr]

        # --------------------------------------------------------
        # Two-qubit (controlled) gate: e.g. "CNOT1-3"
        # --------------------------------------------------------
        elif len(parts) == 2:
            control, target = map(int, parts)

            # Normalize synonyms, e.g. CX → CNOT
            gate_name = 'CNOT' if name in ('CNOT', 'CX') else name

            instr = Instruction(name=gate_name, targets=[target], controls=[control])
            instructions = [instr]

        else:
            raise ValueError(
                f"Token '{token}' has an invalid qubit format with too many dashes."
            )

        # --------------------------------------------------------
        # Decomposition of non-Clifford+T gates (unitary only)
        # --------------------------------------------------------
        # At this point, MEASURE has already been handled, so the gate
        # must be unitary. If its name is not in the allowed Clifford+T
        # set, we require a user-supplied decomposition map.
        # --------------------------------------------------------
        allowed_primitive = {'X', 'Y', 'Z', 'H', 'S', 'T', 'CNOT', 'CX'}

        if name not in allowed_primitive:
            if name in self.decomposition_map:
                return self.decomposition_map[name]
            else:
                raise ValueError(
                    f"Gate '{name}' is not part of the Clifford+T set and has no "
                    f"decomposition rule in the provided decomposition map."
                )

        return instructions

    def parse_tokens(self, tokens: List[str]) -> List[Instruction]:
        """
        Parse a list of string tokens into a flat list of Instruction objects.

        :param tokens: List of DSL instruction strings.
        :return: List of Instruction objects.
        """
        all_instrs: List[Instruction] = []
        for tok in tokens:
            all_instrs.extend(self.parse(tok))
        return all_instrs
