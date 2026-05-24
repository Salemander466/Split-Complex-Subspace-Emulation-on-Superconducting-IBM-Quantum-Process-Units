import pytest

pytest.importorskip("qiskit")

import numpy as np

from hscq.experiments import build_loopback_circuit, build_crosstalk_circuit


def test_loopback_circuit_builds():
    circuit = build_loopback_circuit(bit=1, theta=np.pi / 4, depth=2)
    assert circuit.num_qubits == 2
    assert circuit.num_clbits == 2
    assert circuit.depth() > 0


def test_crosstalk_circuit_builds():
    circuit = build_crosstalk_circuit(theta=np.pi / 4)
    assert circuit.num_qubits == 4
    assert circuit.num_clbits == 2
