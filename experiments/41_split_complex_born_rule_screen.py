"""Split-Complex Born-Rule Model-Separation Screen.

This script compares a standard RZ phase baseline to the split-complex mapped
operator across basis sweeps. It is a model-separation screen, not by itself a
new-physics proof. The next step after this screen is identical-circuit
hardware-vs-statevector residual analysis.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

from hscq.experiments import build_born_rule_screen_circuit


def probs(counts: dict[str, int]) -> dict[str, float]:
    total = sum(counts.values()) or 1
    return {k: counts.get(k, 0) / total for k in ["00", "01", "10", "11"]}


def same_state_probability(p: dict[str, float]) -> float:
    return p["00"] + p["11"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", default=None)
    parser.add_argument("--shots", type=int, default=10000)
    parser.add_argument("--optimization-level", type=int, default=3)
    parser.add_argument("--token", default=None)
    parser.add_argument("--output", default="born_rule_screen_results.json")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    theta_degrees = list(range(0, 181, 15))
    bases = ["Z", "X", "Y"]
    circuits = []
    metadata = []

    for theta_deg in theta_degrees:
        theta = np.deg2rad(theta_deg)
        for basis in bases:
            for model in ["standard_complex", "split_complex_mapped"]:
                circuits.append(build_born_rule_screen_circuit(model=model, theta=theta, basis=basis))
                metadata.append({"theta_deg": theta_deg, "basis": basis, "model": model})

    print("circuits:", len(circuits))
    if args.dry_run:
        for md, circuit in zip(metadata[:6], circuits[:6]):
            print(md, "depth=", circuit.depth(), "ops=", dict(circuit.count_ops()))
        return

    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=args.token) if args.token else QiskitRuntimeService()
    backend = service.backend(args.backend) if args.backend else service.least_busy(simulator=False, operational=True)
    pass_manager = generate_preset_pass_manager(backend=backend, optimization_level=args.optimization_level)
    isa = [pass_manager.run(c) for c in circuits]

    print("backend:", backend.name)
    print("submitting...")
    job = SamplerV2(backend).run(isa, shots=args.shots)
    results = job.result()

    rows = []
    for i, md in enumerate(metadata):
        counts = results[i].data.c.get_counts()
        p = probs(counts)
        rows.append({
            **md,
            "counts": counts,
            "same_state_probability": same_state_probability(p),
            "probabilities": p,
            "compiled_depth": isa[i].depth(),
            "compiled_ops": dict(isa[i].count_ops()),
        })

    comparisons = []
    by_key = {}
    for row in rows:
        by_key.setdefault((row["theta_deg"], row["basis"]), {})[row["model"]] = row
    for (theta_deg, basis), pair in by_key.items():
        if set(pair) == {"standard_complex", "split_complex_mapped"}:
            a = pair["standard_complex"]["same_state_probability"]
            b = pair["split_complex_mapped"]["same_state_probability"]
            se = np.sqrt(max(1e-12, a * (1 - a) / args.shots) + max(1e-12, b * (1 - b) / args.shots))
            comparisons.append({
                "theta_deg": theta_deg,
                "basis": basis,
                "standard_same_probability": a,
                "split_same_probability": b,
                "delta": b - a,
                "screening_z_score": (b - a) / se,
            })

    payload = {
        "backend": backend.name,
        "job_id": job.job_id(),
        "shots": args.shots,
        "optimization_level": args.optimization_level,
        "rows": rows,
        "comparisons": comparisons,
        "scientific_caveat": "Model separation is not a Born-rule violation. Run identical-circuit statevector residual testing next.",
    }
    Path(args.output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print("saved:", args.output)
    print("largest deviations:")
    for item in sorted(comparisons, key=lambda x: abs(x["screening_z_score"]), reverse=True)[:10]:
        print(item)


if __name__ == "__main__":
    main()
