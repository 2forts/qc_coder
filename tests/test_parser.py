import pytest
from qc_coder.parser import Parser
from qc_coder.gates import Instruction


def test_parse_single_qubit_gate():
    parser = Parser()
    instrs = parser.parse("X2")
    assert isinstance(instrs, list)
    assert len(instrs) == 1
    instr = instrs[0]
    assert instr.name == 'X'
    assert instr.targets == [2]
    assert instr.controls == []
    assert instr.params == []


def test_parse_controlled_gate_cnot():
    parser = Parser()
    instrs = parser.parse("CNOT1-3")
    assert len(instrs) == 1
    instr = instrs[0]
    assert instr.name == 'CNOT'
    assert instr.targets == [3]
    assert instr.controls == [1]


def test_parse_multiple_tokens():
    parser = Parser()
    tokens = ["H0", "T1", "X2"]
    instrs = parser.parse_tokens(tokens)
    names = [instr.name for instr in instrs]
    targets = [instr.targets[0] for instr in instrs]
    assert names == ['H', 'T', 'X']
    assert targets == [0, 1, 2]


def test_parse_invalid_token_format():
    parser = Parser()
    with pytest.raises(ValueError):
        parser.parse("INVALID")
    with pytest.raises(ValueError):
        parser.parse("X-1-2-3")  # too many parts


def test_parse_custom_gate_with_decomposition():
    # Define a custom gate THAT decomposes to H then T on qubit 0
    custom_seq = [Instruction('H', [0]), Instruction('T', [0])]
    parser = Parser(decomposition_map={'MYGATE': custom_seq})
    instrs = parser.parse("MYGATE0")
    assert instrs == custom_seq


def test_parse_custom_gate_without_decomposition_raises():
    parser = Parser()
    with pytest.raises(ValueError) as excinfo:
        parser.parse("MYGATE0")
    assert "no tiene descomposición en el mapa" in str(excinfo.value)
