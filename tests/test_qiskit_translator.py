import pytest
from math import pi
from qc_coder.gates import Instruction
from qc_coder.translator.qiskit_translator import QiskitTranslator

# Skip tests if Qiskit is not installed
def pytest_configure(config):
    pytest.importorskip("qiskit")

def test_translate_x_gate():
    translator = QiskitTranslator(num_qubits=1)
    circuit = translator.translate([Instruction('X', [0])])
    ops = circuit.count_ops()
    assert ops.get('x', 0) == 1

def test_translate_h_gate():
    translator = QiskitTranslator(num_qubits=1)
    circuit = translator.translate([Instruction('H', [0])])
    ops = circuit.count_ops()
    assert ops.get('h', 0) == 1

def test_translate_cnot_gate():
    translator = QiskitTranslator(num_qubits=2)
    instr = Instruction('CNOT', [1], controls=[0])
    circuit = translator.translate([instr])
    ops = circuit.count_ops()
    assert ops.get('cx', 0) == 1

def test_translate_rx_and_rz_gates():
    translator = QiskitTranslator(num_qubits=1)
    angle_rx = pi / 4
    circuit_rx = translator.translate([Instruction('RX', [0], params=[angle_rx])])
    ops_rx = circuit_rx.count_ops()
    assert ops_rx.get('rx', 0) == 1

    angle_rz = pi / 2
    circuit_rz = translator.translate([Instruction('RZ', [0], params=[angle_rz])])
    ops_rz = circuit_rz.count_ops()
    assert ops_rz.get('rz', 0) == 1

def test_unsupported_gate_raises_value_error():
    translator = QiskitTranslator(num_qubits=1)
    with pytest.raises(ValueError):
        translator.translate([Instruction('FOO', [0])])
