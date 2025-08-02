# qc_coder

**Método y sistema implementado por ordenador para la codificación eficiente de circuitos cuánticos mediante entrada simbólica estructurada**

Un paquete Python ligero para parsear instrucciones simbólicas de puertas cuánticas basadas en Clifford+T, y generar circuitos en múltiples frameworks (Qiskit, Cirq, Braket) de forma rápida y unificada.

---

## 🔍 Características

- **Parser de tokens**: convierte cadenas como `X2`, `CNOT1-3`, `T0` en objetos de instrucción.
- **Soporte Clifford+T**: maneja puertas estándar (X, Y, Z, H, S, T, CNOT) y permite descomponer puertas personalizadas en secuencias de Clifford+T.
- **Traductores específicos**: genera circuitos en:
  - Qiskit
  - Cirq
  - Amazon Braket SDK
- **Interfaz unificada**: `UnifiedInterface` orquesta parsing y traducción según el framework elegido.
- **Configuración extensible**: mapa de descomposiciones en JSON/YAML opcional.

---

## 📁 Estructura del proyecto

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
└── example_usage.py

setup.py
requirements.txt
README.md
LICENSE

# OPTIONAL
config/decomposition_map.json
tests/
``` 

---

## ⚙️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/qc_coder.git
   cd qc_coder
   ```
2. Crea y activa un entorno virtual (opcional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate    # Windows
   ```
3. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Uso básico

```python
from qc_coder.interface import UnifiedInterface

# Inicializa con Qiskit, 4 qubits y un mapa de descomposición opcional
ui = UnifiedInterface(
    framework='qiskit',
    num_qubits=4,
    decomposition_map={
        'MYGATE': [Instruction('H', [0]), Instruction('T', [0])]
    }
)

# Define instrucciones simbólicas
tokens = ['H0', 'CNOT0-1', 'T1', 'X2', 'MYGATE0']

# Construye el circuito
circuit = ui.build_circuit(tokens)
print(circuit)
```

---

## 🛠️ Configuración de descomposiciones

Para puertas no Clifford+T, crea un archivo JSON (`config/decomposition_map.json`):

```json
{
  "MYGATE": [
    {"name": "H", "targets": [0], "controls": [], "params": []},
    {"name": "T", "targets": [0], "controls": [], "params": []}
  ]
}
```

Y pásalo al inicializar:

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

## 🤝 Contribuciones

1. Haz un fork del repositorio.
2. Crea una rama con tu feature: `git checkout -b feature/nueva-puerta`.
3. Haz commit de tus cambios: `git commit -m 'Añade descomposición de puerta'`.
4. Abre un Pull Request.

---

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.
