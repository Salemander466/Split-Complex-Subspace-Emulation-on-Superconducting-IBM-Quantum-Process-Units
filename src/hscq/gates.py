"""Core circuit construction utilities for split-complex subspace experiments."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit import Gate

LogicalBit = Literal[0, 1]


def split_complex_gate(theta: float, inverse: bool = False, name: str = "SplitComplexGate") -> Gate:
    """Return the two-qubit mapped split-complex emulation gate.

    The decomposition used throughout the validation suite is:
        CX -> RY(2 * theta) -> CX

    The inverse uses -theta. This is a standard Hilbert-space circuit
    representation; it is not a claim of non-standard quantum mechanics.
    """
    qr = QuantumRegister(2, "q")
    circuit = QuantumCircuit(qr, name=name)
    angle = -theta if inverse else theta
    circuit.cx(qr[0], qr[1])
    circuit.ry(2 * angle, qr[0])
    circuit.cx(qr[0], qr[1])
    return circuit.to_gate()


def initialize_logical_bit(circuit: QuantumCircuit, qubits, bit: LogicalBit) -> None:
    """Encode logical 0 as |00> and logical 1 as |11>."""
    if bit not in (0, 1):
        raise ValueError("bit must be 0 or 1")
    if bit == 1:
        circuit.x(qubits[0])
        circuit.x(qubits[1])


def target_state(bit: LogicalBit) -> str:
    return "11" if bit == 1 else "00"


def fidelity_from_counts(counts: dict[str, int], target: str, shots: int) -> float:
    if shots <= 0:
        raise ValueError("shots must be positive")
    return 100.0 * counts.get(target, 0) / shots
