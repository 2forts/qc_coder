from typing import List, Optional


class Instruction:
    """
    Representa una instrucción de puerta cuántica.

    Attributes:
        name (str): Nombre de la puerta (ej. 'X', 'H', 'CNOT').
        targets (List[int]): Índices de los qubits objetivo.
        controls (List[int]): Índices de los qubits de control, si aplica.
        params (List[float]): Parámetros de la puerta (p.ej. ángulos de rotación).
    """
    def __init__(self,
                 name: str,
                 targets: List[int],
                 controls: Optional[List[int]] = None,
                 params: Optional[List[float]] = None):
        self.name = name
        self.targets = targets
        self.controls = controls if controls is not None else []
        self.params = params if params is not None else []

    def __repr__(self) -> str:
        ctrl = f" controls={self.controls}" if self.controls else ""
        prm = f" params={self.params}" if self.params else ""
        return f"Instruction(name='{self.name}', targets={self.targets}{ctrl}{prm})"
