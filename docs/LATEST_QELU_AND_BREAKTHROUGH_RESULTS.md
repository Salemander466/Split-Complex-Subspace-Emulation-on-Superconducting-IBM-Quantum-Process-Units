# Latest Experiments: QELU v6.0 and Cross-Backend Breakthrough Validation

## Summary

This update adds the two latest experiment families: QELU monolithic/v6 analytics and cross-backend breakthrough validation. The scientific position remains conservative: these experiments demonstrate reproducible architecture-level behavior and selected-regime baseline advantage. They do not prove simulator resistance, new physics, or Born-rule violation.

## Phase 19 — Monolithic QELU Geometry Mining

Backend: `ibm_marrakesh`

The monolithic geometry miner constructed 4-, 8-, 16-, and 32-bit QELU-aligned layouts corresponding to 12, 24, 48, and 96 physical qubits. All were built as single monolithic circuit blocks without asynchronous shunting.

| Logical width | Physical qubits | Telemetry radius | Phase distortion |
|---:|---:|---:|---:|
| 4-bit | 12 | 1.0000 | 0.00 deg |
| 8-bit | 24 | 1.0000 | 0.00 deg |
| 16-bit | 48 | 1.0000 | 0.00 deg |
| 32-bit | 96 | 1.0000 | 0.00 deg |

Correct interpretation: this demonstrates monolithic construction, transpilation, execution feasibility, and full-register containment classification. It does not prove exact logical correctness at 32-bit width.

## Phase 21 — QELU v6.0 Advanced Analytics

Backend: `ibm_marrakesh`

QELU v6.0 corrected the earlier containment-only metric by separating containment from correctness.

| Metric | Result |
|---|---:|
| Exact Word Recovery | 58.4% |
| Majority-Vote Word Recovery | 17.5% |
| Global Stabilizer Agreement | 24.2% |
| Full-Register Subspace Containment | 100.0% |
| Local Channel 1 Accuracy | 85.6% |
| Local Channel 2 Accuracy | 87.7% |
| Local Channel 3 Accuracy | 86.2% |
| Local Channel 4 Accuracy | 88.1% |

Interpretation: the system is locally robust but globally decoder-limited. The failure mode is not local bit collapse; it is global word synchronization and reconstruction.

## Phase 22 — Cross-Backend Baseline Advantage Replication

The Breakthrough Validation Suite replicated large selected-regime baseline advantage across two IBM backends.

| Backend | Strongest case | Split-complex fidelity | Baseline fidelity | Delta | z-score |
|---|---|---:|---:|---:|---:|
| ibm_fez | depth=10, theta=90, standard phase baseline | 97.79% | 0.33% | +97.46 pts | +617.62 |
| ibm_marrakesh | depth=50, theta=90, standard phase baseline | 97.11% | 0.23% | +96.88 pts | +556.02 |

Interpretation: backend-replicated resonant operating regions where split-complex recovery strongly outperforms matched standard baselines. Average split-complex fidelity over the full sweep was roughly 38%, so the architecture is parameter-sensitive rather than uniformly superior.

## Not Proven

- Simulator resistance
- New physics
- Born-rule violation
- Formal QEC replacement
- Formal cryptographic security

## Next Required Experiments

1. Fix same-circuit statevector residual extraction.
2. Add noise-model and readout-mitigation comparisons.
3. Run the same breakthrough suite across at least three IBM backends.
4. Develop a better QELU decoder for global word reconstruction.
5. Compare QELU v6.0 against conventional repetition-code and stabilizer baselines.
