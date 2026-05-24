"""Runtime helpers for IBM Quantum execution.

The package does not store credentials. Set IBM_QUANTUM_TOKEN in the environment
or pass a token explicitly when creating a runtime service.
"""
from __future__ import annotations

import os
from typing import Optional


def get_ibm_token(explicit_token: Optional[str] = None) -> str:
    token = explicit_token or os.getenv("IBM_QUANTUM_TOKEN")
    if not token:
        raise RuntimeError(
            "IBM Quantum token missing. Set IBM_QUANTUM_TOKEN or pass token explicitly."
        )
    return token


def create_service(token: Optional[str] = None):
    from qiskit_ibm_runtime import QiskitRuntimeService
    return QiskitRuntimeService(channel="ibm_quantum_platform", token=get_ibm_token(token))


def select_backend(service, backend_name: Optional[str] = None):
    if backend_name:
        return service.backend(backend_name)
    return service.least_busy(simulator=False, operational=True)
