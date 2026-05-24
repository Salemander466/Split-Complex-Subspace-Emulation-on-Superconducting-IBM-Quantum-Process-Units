"""Command line interface for local circuit inspection."""
from __future__ import annotations

import argparse
import json
import numpy as np

from .experiments import (
    build_adversarial_recovery_circuit,
    build_born_rule_screen_circuit,
    build_crosstalk_circuit,
    build_loopback_circuit,
    build_qelu_circuit,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and inspect HSCQ validation circuits.")
    parser.add_argument(
        "experiment",
        choices=["loopback", "crosstalk", "adversarial", "qelu", "born-screen"],
    )
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--theta", type=float, default=np.pi / 4)
    parser.add_argument("--bit", type=int, choices=[0, 1], default=1)
    parser.add_argument("--basis", choices=["X", "Y", "Z"], default="Z")
    parser.add_argument("--model", choices=["standard_complex", "split_complex_mapped"], default="split_complex_mapped")
    parser.add_argument("--input-word", default="1011")
    args = parser.parse_args()

    if args.experiment == "loopback":
        circuit = build_loopback_circuit(bit=args.bit, theta=args.theta, depth=args.depth)
    elif args.experiment == "crosstalk":
        circuit = build_crosstalk_circuit(theta=args.theta)
    elif args.experiment == "adversarial":
        circuit = build_adversarial_recovery_circuit(bit=args.bit, theta=args.theta, cycles=args.depth)
    elif args.experiment == "qelu":
        circuit = build_qelu_circuit(input_word=args.input_word, theta=args.theta)
    else:
        circuit = build_born_rule_screen_circuit(model=args.model, theta=args.theta, basis=args.basis)

    payload = {
        "experiment": args.experiment,
        "depth": circuit.depth(),
        "size": circuit.size(),
        "operations": dict(circuit.count_ops()),
        "qubits": circuit.num_qubits,
        "clbits": circuit.num_clbits,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
