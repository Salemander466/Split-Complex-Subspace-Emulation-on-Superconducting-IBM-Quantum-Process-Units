# Updated Report Notes 3: Conceptual Phase Mapping

## Purpose

This report links each chronological experimental phase to the conceptual theory, assumption, or scientific framework it supports or challenges. It merges the phase-results index with the theory-mapping index.

## Scientific Position

The experiments demonstrate reproducible QPU-executable split-complex subspace emulation behavior, not proof of new physics, formal QEC replacement, physical pulse compression, or cryptographic security.

## Executive Summary

The project currently supports three defensible claims:

1. Split-complex and contradiction-tolerant logical structures can be emulated reproducibly in ordinary quantum circuits.
2. Several recovery behaviors align conceptually with operator-algebra QEC, noiseless subsystems, holographic QEC analogies, and Deutsch-style consistency simulation.
3. The evidence challenges narrow assumptions about what can run on NISQ hardware, but it does not prove new physics, real CTCs, physical wormholes, or formal QEC replacement.

# Phase 1 — Foundational Mapping Discovery

Initial construction of a split-complex logical mapping inside ordinary complex Hilbert-space quantum circuits.

## Test: Split-Complex Gate Mapping Prototype

**Backend:** local simulator / conceptual circuit

**What was tested:** Whether split-complex-style transformations could be represented as two-qubit reversible quantum operators.

**Result:** Functional mapping primitive established: CX -> RY(theta) -> CX.

**Score:** None

**Interpretation:** Established the base compiler primitive used throughout the project.

**Caveat:** This is an emulation layer, not physical realization of split-complex particles.

**Conceptual links:**

- **Split-complex logic is only mathematical and not executable on physical quantum hardware.** (Challenged; challenged_assumption)
  - Evidence link: Split-complex-inspired mappings were executed reproducibly on IBM superconducting hardware with high recovery fidelity.
  - Not yet proven: This does not establish physical split-complex particles or nonstandard quantum mechanics.
  - APA7: Khrennikov, A. (2003). Hyperbolic quantum mechanics. Advances in Applied Clifford Algebras, 13(1), 1–9.

---

# Phase 2 — Initial Hardware Recovery Validation

First real-QPU tests showing that reversible mapped states could be recovered after transformation.

## Test: Bell-State / Payload Recovery

**Backend:** IBM Quantum hardware

**What was tested:** Recovery of payload states after reversible scrambling and inverse transformation.

**Result:** High-fidelity recovery observed.

**Score:** Above 98% in early recovery runs

**Interpretation:** Demonstrated that the mapped architecture could execute on real superconducting hardware.

**Caveat:** Exact backend and post-transpile audit should be recorded for each run.

**Conceptual links:**

- **Split-complex logic is only mathematical and not executable on physical quantum hardware.** (Challenged; challenged_assumption)
  - Evidence link: Split-complex-inspired mappings were executed reproducibly on IBM superconducting hardware with high recovery fidelity.
  - Not yet proven: This does not establish physical split-complex particles or nonstandard quantum mechanics.
  - APA7: Khrennikov, A. (2003). Hyperbolic quantum mechanics. Advances in Applied Clifford Algebras, 13(1), 1–9.

---

# Phase 3 — Hardware Cryptographic Pipeline Tests

End-to-end data ingestion, transformation, inverse recovery, and readout pipeline.

## Test: End-to-End Reversible Payload Pipeline

**Backend:** IBM Quantum hardware

**What was tested:** Whether a classical payload bit could be transformed and recovered through the split-complex reversible pipeline.

**Result:** Payload recovered with high fidelity.

**Score:** 98.6% in reported cryptographic loopback run

**Interpretation:** Supported the claim that the architecture can perform stable reversible payload recovery.

**Caveat:** This does not prove formal cryptographic security.

**Conceptual links:**

- **Split-complex logic is only mathematical and not executable on physical quantum hardware.** (Challenged; challenged_assumption)
  - Evidence link: Split-complex-inspired mappings were executed reproducibly on IBM superconducting hardware with high recovery fidelity.
  - Not yet proven: This does not establish physical split-complex particles or nonstandard quantum mechanics.
  - APA7: Khrennikov, A. (2003). Hyperbolic quantum mechanics. Advances in Applied Clifford Algebras, 13(1), 1–9.

---

# Phase 4 — Compiler Interaction Discovery

Discovery that the Qiskit transpiler aggressively compresses reversible structures and that compiler behavior is part of the architecture.

## Test: QEC / Reversible Compression Benchmark

**Backend:** ibm_marrakesh

**What was tested:** Comparison of structured reversible mapping against an unstructured baseline under repeated transformation loops.

**Result:** Structured mapping retained 99.0% fidelity while baseline showed 63.0%.

**Score:** 99.0% structured fidelity; 63.0% baseline fidelity

**Interpretation:** Showed favorable compiler simplification and recovery stability for the structured mapping.

**Caveat:** Should be described as transpiler-level reduction unless pulse schedules verify physical compression.

**Conceptual links:**

- **Operator-Algebra Quantum Error Correction** (Strongly Related; supported_theory)
  - Evidence link: Information behaved like recoverable subsystem-style encoding under corruption.
  - Not yet proven: Formal operator-algebra code-distance scaling has not yet been measured.
  - APA7: Kribs, D. W., Laflamme, R., Poulin, D., & Lesosky, M. (2005). Operator quantum error correction. Quantum Information & Computation, 6(4), 382–399.
- **Noiseless Subsystems / Decoherence-Free Subspaces** (Potentially Supported; supported_theory)
  - Evidence link: The mapped subspace showed unusually stable recovery under several noise and sabotage conditions.
  - Not yet proven: Controlled noise-channel characterization has not yet been completed.
  - APA7: Lidar, D. A., Chuang, I. L., & Whaley, K. B. (1998). Decoherence-free subspaces for quantum computation. Physical Review Letters, 81(12), 2594–2597.

---

# Phase 5 — Deflector Hook Experiment

Adversarial compiler-resistance test forcing nontrivial physical execution.

## Test: Deflector Hook Resource Audit

**Backend:** ibm_marrakesh

**What was tested:** Whether randomized basis switching and phase perturbations could prevent full symbolic cancellation.

**Result:** Native operations survived transpilation: rz=22, sx=20, cz=4, measure=2, barrier=1; compiled depth=29; circuit size=48.

**Score:** 4 native CZ gates retained; depth 29

**Interpretation:** The compiler could not erase the adversarial logic entirely, supporting nontrivial hardware execution.

**Caveat:** Still requires statevector and noise-model comparison for physical interpretation.

**Conceptual links:**

- **Deep reversible circuits necessarily collapse rapidly on NISQ devices.** (Challenged; challenged_assumption)
  - Evidence link: 97.8% fidelity remained at 100,000 programmed gate-pair depth.
  - Not yet proven: Physical pulse depth and scheduled-duration immunity have not been established.
  - APA7: Preskill, J. (2018). Quantum computing in the NISQ era and beyond. Quantum, 2, 79.

---

# Phase 6 — Destructive Depth-Limit Validation

Stress-to-failure test scaling nominal programmed depth to extreme forward/reverse gate-pair counts.

## Test: Destructive Depth-Limit Stress Test

**Backend:** ibm_kingston

**What was tested:** Forward and inverse split-complex chains at 1,000, 10,000, and 100,000 programmed gate-pair depths.

**Result:** Fidelity remained high across all programmed depths.

**Score:**

- 1000_pairs: 98.2%
- 10000_pairs: 98.4%
- 100000_pairs: 97.8%

**Interpretation:** Nominal programmed depth did not materially degrade recovery in this reversible compiled workload.

**Caveat:** Must log post-transpile physical depth, native gate counts, and scheduled duration before claiming physical depth immunity.

**Conceptual links:**

- **Deep reversible circuits necessarily collapse rapidly on NISQ devices.** (Challenged; challenged_assumption)
  - Evidence link: 97.8% fidelity remained at 100,000 programmed gate-pair depth.
  - Not yet proven: Physical pulse depth and scheduled-duration immunity have not been established.
  - APA7: Preskill, J. (2018). Quantum computing in the NISQ era and beyond. Quantum, 2, 79.

---

# Phase 7 — Holographic Information Recovery Experiments

Reversible scrambling and reconstruction experiments framed as computational holographic analogies.

## Test: ER/EPR Traversal Emulator

**Backend:** ibm_marrakesh

**What was tested:** Two-qubit holographic-style scrambling, shockwave inversion, and target-state reconstruction.

**Result:** Stable recovery after reversible scrambling.

**Score:** 98.9% signal recovery

**Interpretation:** Showed stable nonlocal-style recovery behavior in ordinary quantum circuits.

**Caveat:** Does not claim physical wormholes or gravitational spacetime.

**Conceptual links:**

- **Holographic Quantum Error Correction** (Architecturally Supported; supported_theory)
  - Evidence link: Local damage and scrambling still allowed nonlocal recovery of the logical payload.
  - Not yet proven: No proof of AdS/CFT, spacetime emergence, or physical wormholes.
  - APA7: Pastawski, F., Yoshida, B., Harlow, D., & Preskill, J. (2015). Holographic quantum error-correcting codes: Toy models for the bulk/boundary correspondence. Journal of High Energy Physics, 2015(6), 149.

---

# Phase 8 — Macro Wide-Throat Scaling

Expansion of the holographic-style recovery layout from two qubits to a wider four-qubit structure.

## Test: Macro Wormhole / 4-Qubit Wide-Throat Simulator

**Backend:** ibm_kingston

**What was tested:** Four-qubit scaled recovery structure with wider entangled register layout.

**Result:** Stable multi-qubit loop-back reconstruction.

**Score:** 97.1% loop-back stability

**Interpretation:** Demonstrated that the architecture could scale beyond the smallest two-qubit toy setting.

**Caveat:** Further scaling showed NISQ width limitations.

**Conceptual links:**

- **Holographic Quantum Error Correction** (Architecturally Supported; supported_theory)
  - Evidence link: Local damage and scrambling still allowed nonlocal recovery of the logical payload.
  - Not yet proven: No proof of AdS/CFT, spacetime emergence, or physical wormholes.
  - APA7: Pastawski, F., Yoshida, B., Harlow, D., & Preskill, J. (2015). Holographic quantum error-correcting codes: Toy models for the bulk/boundary correspondence. Journal of High Energy Physics, 2015(6), 149.

---

# Phase 9 — Compiler-Proof Random Drift Stress

Adversarial randomized perturbation test forcing retained physical execution paths.

## Test: Random Drift Compiler-Proof Stress

**Backend:** ibm_kingston

**What was tested:** Interleaved random angle drifts and asynchronous barriers to prevent trivial optimization.

**Result:** Physical containment survived anti-cancellation design.

**Score:** 94.2% physical containment

**Interpretation:** Recovery remained strong even when the compiler was forced to retain nontrivial native operations.

**Caveat:** Still requires exact circuit-by-circuit simulator residual comparison.

**Conceptual links:**

- **Deep reversible circuits necessarily collapse rapidly on NISQ devices.** (Challenged; challenged_assumption)
  - Evidence link: 97.8% fidelity remained at 100,000 programmed gate-pair depth.
  - Not yet proven: Physical pulse depth and scheduled-duration immunity have not been established.
  - APA7: Preskill, J. (2018). Quantum computing in the NISQ era and beyond. Quantum, 2, 79.

---

# Phase 10 — Dynamic Conditional Trap

Runtime conditional branching test using mid-circuit measurement and if_test control flow.

## Test: Dynamic Conditional Trap

**Backend:** ibm_kingston

**What was tested:** Mid-circuit measurement branching designed to defeat trivial compiler cancellation.

**Result:** Runtime control-flow circuit recovered payload above random baseline.

**Score:** 82.6% runtime fidelity

**Interpretation:** One of the hardest tests; demonstrated survivable dynamic control flow.

**Caveat:** Lower fidelity marks a real architectural boundary.

**Conceptual links:**

- **Deutsch Closed Timelike Curve Consistency** (Partially Supported; supported_theory)
  - Evidence link: The chronology-loop experiment stabilized into a mixed-state equilibrium rather than random collapse under causal-feedback conditions.
  - Not yet proven: No physical closed timelike curves or time travel were demonstrated.
  - APA7: Deutsch, D. (1991). Quantum mechanics near closed timelike lines. Physical Review D, 44(10), 3197–3217.

---

# Phase 11 — Statistical Confidence Validation

Bootstrap profiling to quantify uncertainty around observed high-fidelity recovery.

## Test: Bootstrap Sample Profiler

**Backend:** ibm_marrakesh

**What was tested:** 2,000-shot high-density run resampled over 2,000 bootstrap loops.

**Result:** Statistical confidence quantified.

**Score:** +/-0.313% standard error

**Interpretation:** Recovery behavior was measurable with statistical uncertainty, not merely anecdotal.

**Caveat:** Every major result should eventually receive comparable confidence intervals.

**Conceptual links:**

- **Noiseless Subsystems / Decoherence-Free Subspaces** (Potentially Supported; supported_theory)
  - Evidence link: The mapped subspace showed unusually stable recovery under several noise and sabotage conditions.
  - Not yet proven: Controlled noise-channel characterization has not yet been completed.
  - APA7: Lidar, D. A., Chuang, I. L., & Whaley, K. B. (1998). Decoherence-free subspaces for quantum computation. Physical Review Letters, 81(12), 2594–2597.

---

# Phase 12 — Horizon Evaporation and Phase-Erasure Tests

Active phase-erasure drift introduced during recovery traversal.

## Test: In-Flight Horizon Evaporation

**Backend:** ibm_marrakesh

**What was tested:** Recovery under injected 0.040 radian phase-erasure drift.

**Result:** Payload restored under active phase-loss conditions.

**Score:** 98.3% data restoration

**Interpretation:** Demonstrated robust recovery under induced phase degradation.

**Caveat:** This is a quantum-information analogy, not physical black-hole evaporation.

**Conceptual links:**

- **Noiseless Subsystems / Decoherence-Free Subspaces** (Potentially Supported; supported_theory)
  - Evidence link: The mapped subspace showed unusually stable recovery under several noise and sabotage conditions.
  - Not yet proven: Controlled noise-channel characterization has not yet been completed.
  - APA7: Lidar, D. A., Chuang, I. L., & Whaley, K. B. (1998). Decoherence-free subspaces for quantum computation. Physical Review Letters, 81(12), 2594–2597.
- **Holographic Quantum Error Correction** (Architecturally Supported; supported_theory)
  - Evidence link: Local damage and scrambling still allowed nonlocal recovery of the logical payload.
  - Not yet proven: No proof of AdS/CFT, spacetime emergence, or physical wormholes.
  - APA7: Pastawski, F., Yoshida, B., Harlow, D., & Preskill, J. (2015). Holographic quantum error-correcting codes: Toy models for the bulk/boundary correspondence. Journal of High Energy Physics, 2015(6), 149.

---

# Phase 13 — Shapiro Delay and Competing Shockwave Experiments

Stacked competing transformations used to test phase tracking under interference.

## Test: Multi-Shockwave Shapiro Time-Delay Metric

**Backend:** ibm_marrakesh

**What was tested:** Positive-energy-style operation followed by inverse recovery operation.

**Result:** Recovered under competing transformation interference.

**Score:** 86.3% phase-tracking accuracy

**Interpretation:** Established recovery under stacked nonlocal-style transformation pressure.

**Caveat:** Computational analogy only; no physical spacetime metric claim.

**Conceptual links:**

- **Holographic Quantum Error Correction** (Architecturally Supported; supported_theory)
  - Evidence link: Local damage and scrambling still allowed nonlocal recovery of the logical payload.
  - Not yet proven: No proof of AdS/CFT, spacetime emergence, or physical wormholes.
  - APA7: Pastawski, F., Yoshida, B., Harlow, D., & Preskill, J. (2015). Holographic quantum error-correcting codes: Toy models for the bulk/boundary correspondence. Journal of High Energy Physics, 2015(6), 149.

---

# Phase 14 — Deutsch Chronology Loop Tests

Mid-circuit measurement and conditional feedback used to emulate chronology-style consistency loops.

## Test: Deutsch Chronology Loop Consistency Ceiling

**Backend:** ibm_marrakesh

**What was tested:** Closed-timelike-loop analogy using future measurement feedback into conditional control flow.

**Result:** Stable mixed-state equilibrium rather than total collapse.

**Score:** 49.1% loop self-consistency

**Interpretation:** Produced a stable split distribution under causal-feedback-style execution.

**Caveat:** Does not prove physical CTCs or time travel.

**Conceptual links:**

- **Deutsch Closed Timelike Curve Consistency** (Partially Supported; supported_theory)
  - Evidence link: The chronology-loop experiment stabilized into a mixed-state equilibrium rather than random collapse under causal-feedback conditions.
  - Not yet proven: No physical closed timelike curves or time travel were demonstrated.
  - APA7: Deutsch, D. (1991). Quantum mechanics near closed timelike lines. Physical Review D, 44(10), 3197–3217.

---

# Phase 15 — Many-Body Sabotage Recovery

Boundary and many-body sabotage experiments testing recovery under deliberate channel corruption.

## Test: Bulk Subspace Sabotage / Boundary Qubit Attack

**Backend:** ibm_marrakesh

**What was tested:** Pauli-X and Pauli-Z sabotage of boundary qubit during active holographic-style traversal.

**Result:** Payload projected into stable alternate mirrored coordinate.

**Score:** 98.0% mirrored containment

**Interpretation:** Local sabotage did not randomize the full logical payload.

**Caveat:** Should be framed as nonlocal recovery behavior, not literal extra-dimensional shielding.

**Conceptual links:**

- **Holographic Quantum Error Correction** (Architecturally Supported; supported_theory)
  - Evidence link: Local damage and scrambling still allowed nonlocal recovery of the logical payload.
  - Not yet proven: No proof of AdS/CFT, spacetime emergence, or physical wormholes.
  - APA7: Pastawski, F., Yoshida, B., Harlow, D., & Preskill, J. (2015). Holographic quantum error-correcting codes: Toy models for the bulk/boundary correspondence. Journal of High Energy Physics, 2015(6), 149.
- **Operator-Algebra Quantum Error Correction** (Strongly Related; supported_theory)
  - Evidence link: Information behaved like recoverable subsystem-style encoding under corruption.
  - Not yet proven: Formal operator-algebra code-distance scaling has not yet been measured.
  - APA7: Kribs, D. W., Laflamme, R., Poulin, D., & Lesosky, M. (2005). Operator quantum error correction. Quantum Information & Computation, 6(4), 382–399.

---

## Test: Many-Body Sabotage Recovery

**Backend:** ibm_marrakesh

**What was tested:** Entangled many-body state exposed to ruptured mid-transit channel.

**Result:** Partial channel corruption survived with strong containment.

**Score:** 92.4% mirror containment

**Interpretation:** Demonstrated resilience under deliberate entangled-channel disruption.

**Caveat:** Requires comparison against randomized baseline sabotage circuits.

**Conceptual links:**

- **Operator-Algebra Quantum Error Correction** (Strongly Related; supported_theory)
  - Evidence link: Information behaved like recoverable subsystem-style encoding under corruption.
  - Not yet proven: Formal operator-algebra code-distance scaling has not yet been measured.
  - APA7: Kribs, D. W., Laflamme, R., Poulin, D., & Lesosky, M. (2005). Operator quantum error correction. Quantum Information & Computation, 6(4), 382–399.
- **Noiseless Subsystems / Decoherence-Free Subspaces** (Potentially Supported; supported_theory)
  - Evidence link: The mapped subspace showed unusually stable recovery under several noise and sabotage conditions.
  - Not yet proven: Controlled noise-channel characterization has not yet been completed.
  - APA7: Lidar, D. A., Chuang, I. L., & Whaley, K. B. (1998). Decoherence-free subspaces for quantum computation. Physical Review Letters, 81(12), 2594–2597.

---

# Phase 16 — Crowning Discovery: Quantum Embedded Logic Units

Transition from abstract recovery demonstrations into active low-width embedded computation.

## Test: Fault-Tolerant 4-Bit Quantum Embedded Logic Unit

**Backend:** ibm_marrakesh

**What was tested:** 4-bit input word encoded across 12 physical qubits with sabotage injection and Toffoli-based correction.

**Result:** Original word recovered above random baseline after active sabotage.

**Score:** 83.3% execution accuracy

**Interpretation:** Demonstrated a low-width embedded logic architecture survivable under NISQ fault conditions.

**Caveat:** Does not prove scalable universal fault-tolerant quantum computing.

**Conceptual links:**

- **Operator-Algebra Quantum Error Correction** (Strongly Related; supported_theory)
  - Evidence link: Information behaved like recoverable subsystem-style encoding under corruption.
  - Not yet proven: Formal operator-algebra code-distance scaling has not yet been measured.
  - APA7: Kribs, D. W., Laflamme, R., Poulin, D., & Lesosky, M. (2005). Operator quantum error correction. Quantum Information & Computation, 6(4), 382–399.
- **Useful contradiction-tolerant logic cannot run on NISQ hardware.** (Challenged; challenged_assumption)
  - Evidence link: Belnap-style contradiction-tolerant logical structures were represented and recovered on real QPUs.
  - Not yet proven: No large-scale computational advantage has yet been demonstrated.
  - APA7: Belnap, N. D. (1977). A useful four-valued logic. In Modern uses of multiple-valued logic (pp. 8–37). Springer.

---

## Test: 4-Bit QEC Bus Boundary Core

**Backend:** ibm_marrakesh / ibm_fez

**What was tested:** Word-width scaling and QEC-bus containment under active sabotage.

**Result:** 4-bit / 6-bit region identified as practical NISQ sweet spot.

**Score:** 77.1% to 79.7% boundary-core containment

**Interpretation:** Located useful low-width operational regime before coherence wall effects dominate.

**Caveat:** Higher widths degraded sharply on current NISQ hardware.

**Conceptual links:**

- **Operator-Algebra Quantum Error Correction** (Strongly Related; supported_theory)
  - Evidence link: Information behaved like recoverable subsystem-style encoding under corruption.
  - Not yet proven: Formal operator-algebra code-distance scaling has not yet been measured.
  - APA7: Kribs, D. W., Laflamme, R., Poulin, D., & Lesosky, M. (2005). Operator quantum error correction. Quantum Information & Computation, 6(4), 382–399.

---

# Phase 17 — Classical Word-Width Hardware Scaling

Grid search over classical computing word widths to identify NISQ width limits and shunting workaround.

## Test: 4/8/16/32/64-Bit Width Scaling Search

**Backend:** ibm_fez / ibm_marrakesh

**What was tested:** Fault-tolerant logic scaling across classical word widths.

**Result:** 6-bit / 4-bit QEC bus was usable; 16-bit and 32-bit widths hit NISQ coherence wall.

**Score:** 79.7% boundary core; 77.1% 4-bit QEC bus; 13.3% at 16-bit; 1.4% at 32-bit

**Interpretation:** Mapped the practical width boundary and motivated asynchronous subspace shunting.

**Caveat:** Shunting is architectural emulation, not proof that a physical 156-qubit device executed a full 192-track machine natively.

**Conceptual links:** No direct conceptual mapping assigned yet.

---

# Phase 18 — Born-Rule Deviation Screening

Model-separation test comparing split-complex mapped operator against standard RZ phase baseline.

## Test: Split-Complex Born-Rule Deviation Screen

**Backend:** ibm_kingston

**What was tested:** 78 circuits across 13 theta angles and X/Y/Z bases with anti-cancellation perturbations.

**Result:** Large model separation between standard RZ baseline and split-complex mapped operator.

**Score:**

- largest_case: theta=180 deg, basis=X
- standard_same_probability: 2.27%
- split_same_probability: 97.91%
- delta: 95.64 percentage points
- z_score: 463.12

**Interpretation:** Confirmed that the mapped operator is not behaviorally equivalent to a simple complex RZ phase baseline.

**Caveat:** This is not yet a standard quantum mechanics violation; next step is same-circuit hardware-vs-statevector residual analysis.

**Conceptual links:**

- **Split-complex logic is only mathematical and not executable on physical quantum hardware.** (Challenged; challenged_assumption)
  - Evidence link: Split-complex-inspired mappings were executed reproducibly on IBM superconducting hardware with high recovery fidelity.
  - Not yet proven: This does not establish physical split-complex particles or nonstandard quantum mechanics.
  - APA7: Khrennikov, A. (2003). Hyperbolic quantum mechanics. Advances in Applied Clifford Algebras, 13(1), 1–9.

---

# Reference Index

- Khrennikov, A. (2003). Hyperbolic quantum mechanics. Advances in Applied Clifford Algebras, 13(1), 1–9.
- Belnap, N. D. (1977). A useful four-valued logic. In Modern uses of multiple-valued logic (pp. 8–37). Springer.
- Preskill, J. (2018). Quantum computing in the NISQ era and beyond. Quantum, 2, 79.
- Deutsch, D. (1991). Quantum mechanics near closed timelike lines. Physical Review D, 44(10), 3197–3217.
- Pastawski, F., Yoshida, B., Harlow, D., & Preskill, J. (2015). Holographic quantum error-correcting codes: Toy models for the bulk/boundary correspondence. Journal of High Energy Physics, 2015(6), 149.
- Kribs, D. W., Laflamme, R., Poulin, D., & Lesosky, M. (2005). Operator quantum error correction. Quantum Information & Computation, 6(4), 382–399.
- Lidar, D. A., Chuang, I. L., & Whaley, K. B. (1998). Decoherence-free subspaces for quantum computation. Physical Review Letters, 81(12), 2594–2597.