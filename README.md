# qc_coder

**Method and computer-implemented system for efficient encoding of quantum circuits using structured symbolic input**

A lightweight Python package for parsing symbolic instructions from Clifford+T-based quantum gates and generating circuits in multiple frameworks (Qiskit, Cirq, Braket) quickly and in a unified manner.

If you use this software in your research or projects, please cite the following work:  
Gil‐Serret, R., Ortega, G., & Orts, F. (2026). *A Unified Interface for Framework‐Agnostic Quantum Circuit Construction Based on Tokenized Text Input*. **Software: Practice and Experience**.

---

## 🔍 Features

- **Token parser**: converts strings such as `X2`, `CNOT1-3`, `T0` into instruction objects.
- **Clifford+T support**: handles standard gates (X, Y, Z, H, S, T, CNOT) and allows custom gates to be broken down into sequences of Clifford+T.
- **Specific translators**: generates circuits in:
  - Qiskit
  - Cirq
  - Amazon Braket SDK
- **Unified interface**: `UnifiedInterface` orchestrates parsing and translation according to the chosen framework.
- **Extensible configuration**: optional JSON/YAML decomposition map.

---

## 📁 Project structure

```
qc_coder/
├── __init__.py
├── parser.py
├── gates.py
├── interface.py
└── translator/
    ├── __init__.py
    ├── base.py
    ├── qiskit_translator.py
    ├── cirq_translator.py
    └── braket_translator.py

examples/
├── benchmark_generate_data.py
├── deutsch_jozsa_demo.py
├── example_usage.py
├── grover_demo
├── semantic_equivalence_benchmark.py
└── teleportation_example.py

setup.py
requirements.txt
README.md
LICENSE

# OPTIONAL
config/decomposition_map.json
tests/
``` 

---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tu_usuario/qc_coder.git
   cd qc_coder
   ```
2. Create and activate a virtual environment (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Basic usage

```python
from qc_coder.interface import UnifiedInterface

# Initialize with Qiskit, 4 qubits, and an optional decomposition map
ui = UnifiedInterface(
    framework='qiskit',
    num_qubits=4,
    decomposition_map={
        'MYGATE': [Instruction('H', [0]), Instruction('T', [0])]
    }
)

# Define symbolic instructions
tokens = ['H0', 'CNOT0-1', 'T1', 'X2', 'MYGATE0']

# Build the circuit
circuit = ui.build_circuit(tokens)
print(circuit)
```

---

## 🛠️ Decomposition settings

For non-Clifford+T doors, create a JSON file (`config/decomposition_map.json`):

```json
{
  "MYGATE": [
    {"name": "H", "targets": [0], "controls": [], "params": []},
    {"name": "T", "targets": [0], "controls": [], "params": []}
  ]
}
```

And pass it when initializing:

```python
ui = UnifiedInterface(
    framework='cirq',
    num_qubits=3,
    decomposition_map=load_json('config/decomposition_map.json')
)
```

---

## 🔧 Tests

```bash
pytest tests/
```

---

## 🤝 Contributions

1. Fork the repository.
2. Create a branch with your feature: `git checkout -b feature/new-door`.
3. Commit your changes: `git commit -m ‘Add door decomposition’`.
4. Open a Pull Request.

---

## 📝 License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more details.
