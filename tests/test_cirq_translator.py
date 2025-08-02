import pytest
from math import pi
from gates import Instruction
from translator.cirq_translator import CirqTranslator

# Saltar tests si Cirq no está instalado
def pytest_configure(config):
    pytest.importorskip("cirq")


def count_ops(circuit):
    # Cuenta el número total de operaciones en el circuito
    return sum(1 for _ in circuit.all_operations())


def test_translate_x_gate():
    translator = CirqTranslator(num_qubits=1)
    circuit = translator.translate([Instruction('X', [0])])
    assert count_ops(circuit) == 1


def test_translate_h_gate():
    translator = CirqTranslator(num_qubits=1)
    circuit = translator.translate([Instruction('H', [0])])
    assert count_ops(circuit) == 1


def test_translate_cnot_gate():
    translator = CirqTranslator(num_qubits=2)
    instr = Instruction('CNOT', [1], controls=[0])
    circuit = translator.translate([instr])
    assert count_ops(circuit) == 1


def test_translate_rx_and_rz_gates():
    translator = CirqTranslator(num_qubits=1)
    # RX
    angle_rx = pi / 3
    circuit_rx = translator.translate([Instruction('RX', [0], params=[angle_rx])])
    assert count_ops(circuit_rx) == 1
    # RZ
    angle_rz = pi / 2
    circuit_rz = translator.translate([Instruction('RZ', [0], params=[angle_rz])])
    assert count_ops(circuit_rz) == 1


def test_unsupported_gate_raises_value_error():
    translator = CirqTranslator(num_qubits=1)
    with pytest.raises(ValueError):
        translator.translate([Instruction('FOO', [0])])
