"""Fault-Tolerant 4-Bit Quantum Embedded Logic Unit (QELU).

This script builds and optionally runs the QELU validation circuit. It is a
reproducibility artifact, not a claim of scalable fault-tolerant quantum
computing.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

from hscq.experiments import build_qelu_circuit


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default=None, help="IBM backend name. Defaults to least busy.")
    parser.add_argument("--shots", type=int, default=1000)
    parser.add_argument("--input-word", default="1011")
    parser.add_argument("--token", default=None, help="IBM Quantum token. Prefer env/saved account in production.")
    parser.add_argument("--output", default="qelu_results.json")
    parser.add_argument("--dry-run", action="store_true", help="Only build the circuit and print local metrics.")
    args = parser.parse_args()

    circuit = build_qelu_circuit(args.input_word)
    print("logical circuit depth:", circuit.depth())
    print("logical circuit ops:", dict(circuit.count_ops()))

    if args.dry_run:
        return

    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=args.token) if args.token else QiskitRuntimeService()
    backend = service.backend(args.backend) if args.backend else service.least_busy(simulator=False, operational=True)

    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=3)
    isa = pass_manager.run(circuit)
    print("backend:", backend.name)
    print("compiled depth:", isa.depth())
    print("compiled ops:", dict(isa.count_ops()))

    job = SamplerV2(backend).run([isa], shots=args.shots)
    result = job.result()[0]
    counts = result.data.qelu_bus.get_counts()

    successes = 0
    width = 4
    block = 3
    for bitstring, count in counts.items():
        reversed_bits = bitstring[::-1]
        word = "".join(reversed_bits[i * block] for i in range(width))
        if word == args.input_word:
            successes += count

    accuracy = successes / args.shots
    payload = {
        "backend": backend.name,
        "job_id": job.job_id(),
        "input_word": args.input_word,
        "shots": args.shots,
        "accuracy": accuracy,
        "counts": counts,
        "compiled_depth": isa.depth(),
        "compiled_ops": dict(isa.count_ops()),
    }
    Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
