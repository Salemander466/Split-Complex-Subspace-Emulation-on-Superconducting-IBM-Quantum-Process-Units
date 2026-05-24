"""Reproducible experiment builders for the validation suite.

These functions build circuits but do not submit jobs. This separation makes the
repository testable without IBM Quantum credentials.
"""
from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from .gates import initialize_logical_bit, split_complex_gate


def build_loopback_circuit(bit: int = 1, theta: float = np.pi / 4, depth: int = 1) -> QuantumCircuit:
    q = QuantumRegister(2, "squbit")
    c = ClassicalRegister(2, "secure_bus")
    qc = QuantumCircuit(q, c)
    initialize_logical_bit(qc, q, bit)
    f_gate = split_complex_gate(theta, inverse=False)
    r_gate = split_complex_gate(theta, inverse=True)
    for _ in range(depth):
        qc.append(f_gate, [q[0], q[1]])
    qc.barrier()
    for _ in range(depth):
        qc.append(r_gate, [q[0], q[1]])
    qc.measure(q, c)
    return qc


def build_crosstalk_circuit(theta: float = np.pi / 4) -> QuantumCircuit:
    q = QuantumRegister(4, "hardware_cluster")
    c = ClassicalRegister(2, "secure_bus")
    qc = QuantumCircuit(q, c)
    qc.x(q[0]); qc.x(q[1])
    qc.barrier()
    qc.h(q[2]); qc.x(q[3]); qc.h(q[3])
    qc.append(split_complex_gate(theta), [q[0], q[1]])
    qc.barrier()
    qc.append(split_complex_gate(theta, inverse=True), [q[0], q[1]])
    qc.measure([q[0], q[1]], c)
    return qc


def build_adversarial_recovery_circuit(bit: int = 0, theta: float = np.pi / 3, cycles: int = 25) -> QuantumCircuit:
    q = QuantumRegister(2, "squbit")
    c = ClassicalRegister(2, "secure_bus")
    qc = QuantumCircuit(q, c)
    initialize_logical_bit(qc, q, bit)
    for k in range(cycles):
        eps = ((k % 5) - 2) * 0.003
        qc.append(split_complex_gate(theta + eps), [q[0], q[1]])
        qc.rz(eps, q[0])
        qc.sx(q[1])
        qc.sx(q[1])
    qc.barrier()
    for k in reversed(range(cycles)):
        eps = ((k % 5) - 2) * 0.003
        qc.rz(-eps, q[0])
        qc.append(split_complex_gate(theta + eps, inverse=True), [q[0], q[1]])
    qc.measure(q, c)
    return qc


def build_four_qubit_macro_circuit(theta: float = np.pi / 4, cycles: int = 4) -> QuantumCircuit:
    q = QuantumRegister(4, "macro")
    c = ClassicalRegister(4, "macro_bus")
    qc = QuantumCircuit(q, c)
    for _ in range(cycles):
        qc.append(split_complex_gate(theta), [q[0], q[1]])
        qc.append(split_complex_gate(theta), [q[2], q[3]])
    qc.barrier()
    for _ in range(cycles):
        qc.append(split_complex_gate(theta, inverse=True), [q[0], q[1]])
        qc.append(split_complex_gate(theta, inverse=True), [q[2], q[3]])
    qc.measure(q, c)
    return qc


def build_qelu_circuit(input_word: str = "1011", theta: float = np.pi / 4) -> QuantumCircuit:
    """Build the 4-bit Quantum Embedded Logic Unit validation circuit.

    The circuit uses four 3-qubit repetition frames, injects two intentional
    bit-flip faults, and applies Toffoli-based correction logic.
    """
    if len(input_word) != 4 or set(input_word) - {"0", "1"}:
        raise ValueError("input_word must be a strict 4-bit binary string")

    width = 4
    qubits_per_block = 3
    total_qubits = width * qubits_per_block
    q = QuantumRegister(total_qubits, "qelu_registers")
    c = ClassicalRegister(total_qubits, "qelu_bus")
    qc = QuantumCircuit(q, c)

    for i, bit in enumerate(input_word):
        base = i * qubits_per_block
        if bit == "1":
            qc.x(q[base])
        qc.cx(q[base], q[base + 1])
        qc.cx(q[base], q[base + 2])
    qc.barrier()

    logic_gate = split_complex_gate(theta)
    for i in range(0, total_qubits, 2):
        qc.append(logic_gate, [q[i], q[i + 1]])
    qc.barrier()

    # Intentional mid-transit faults on logical channels 1 and 3.
    qc.x(q[0])
    qc.x(q[6])
    qc.barrier()

    inv_gate = split_complex_gate(theta, inverse=True)
    for i in range(0, total_qubits, 2):
        qc.append(inv_gate, [q[i], q[i + 1]])
    qc.barrier()

    for i in range(width):
        base = i * qubits_per_block
        qc.cx(q[base], q[base + 1])
        qc.cx(q[base], q[base + 2])
        qc.ccx(q[base + 1], q[base + 2], q[base])
    qc.barrier()

    qc.measure([q[i] for i in range(total_qubits)], [c[i] for i in range(total_qubits)])
    return qc


def build_born_rule_screen_circuit(
    model: str = "split_complex_mapped",
    theta: float = np.pi / 4,
    basis: str = "Z",
    anti_cancel: bool = True,
    epsilon: float = 0.005,
) -> QuantumCircuit:
    """Build one circuit for the Born-rule model-separation screen.

    This compares a standard RZ phase baseline against the split-complex mapped
    operator under identical measurement-basis conventions. It is a model
    separation circuit, not a new-physics proof.
    """
    if model not in {"standard_complex", "split_complex_mapped"}:
        raise ValueError("model must be 'standard_complex' or 'split_complex_mapped'")
    if basis not in {"X", "Y", "Z"}:
        raise ValueError("basis must be X, Y, or Z")

    q = QuantumRegister(2, "q")
    c = ClassicalRegister(2, "c")
    qc = QuantumCircuit(q, c, name=model)

    qc.h(q[0])
    qc.cx(q[0], q[1])

    if model == "standard_complex":
        qc.rz(theta, q[0])
        if anti_cancel:
            qc.ry(epsilon, q[1])
            qc.rz(-epsilon, q[0])
    else:
        qc.append(split_complex_gate(theta), [q[0], q[1]])
        if anti_cancel:
            qc.rz(epsilon, q[0])
            qc.ry(-epsilon, q[1])
            qc.sx(q[0])

    if basis == "X":
        qc.h(q[0])
        qc.h(q[1])
    elif basis == "Y":
        qc.sdg(q[0])
        qc.sdg(q[1])
        qc.h(q[0])
        qc.h(q[1])

    qc.measure(q, c)
    return qc
