# Validation Results Table

| # | Test | Backend | What was tested | Score / Result | Status |
|---:|---|---|---|---|---|
| 1 | Ghost gate hardware channel displacement | ibm_marrakesh | A 4x4 ghost gate routed the initialized state into the target hidden bitstring channel on real hardware. | 99.3% target-channel recovery; counts {'10': 993, '00': 6, '11': 1} | pass_with_caveat |
| 2 | End-to-end cryptographic loopback | ibm_marrakesh | Logical bit ingestion, mapped forward transform, inverse recovery, and readout in one hardware job. | 98.6% recovered bit-1 fidelity; 1.4% leakage | pass |
| 3 | Arbitrary split-complex stress sweep | ibm_fez | Three randomized bit/angle recovery trials using the mapped operator and inverse recovery. | 94.2%, 93.9%, and 98.3% fidelity | pass |
| 4 | Circuit depth and coherence stability | ibm_marrakesh | Loopback recovery at programmed depths x2, x4, and x8. | 98.9%, 99.0%, and 98.4% fidelity | pass |
| 5 | Compiler optimization profile | ibm_marrakesh | Execution fidelity across Qiskit transpiler optimization levels 0 through 3. | Level 0: 94.3%; Level 1: 94.2%; Level 2: 98.0%; Level 3: 96.6% | pass |
| 6 | Crosstalk isolation profile | ibm_marrakesh | Two-qubit recovery while neighboring qubits were driven with active H/X interference. | 97.2% fidelity; counts {'11': 972, '01': 15, '10': 11, '00': 2} | pass |
| 7 | Destructive depth-limit stress test | ibm_kingston | Programmed forward/reverse depth scaled to 1,000, 10,000, and 100,000 gate pairs. | 98.2%, 98.4%, and 97.8% fidelity | pass_with_caveat |
| 8 | QEC compression comparison | ibm_marrakesh | Structured reversible workload compared with unstructured baseline under 300 simulated syndrome extraction cycles. | Structured: 99.0%; baseline: 63.0%; both reported 0 post-transpile CX | pass_with_caveat |
| 9 | Adversarial randomized recovery with resource audit | ibm_marrakesh | Randomized bit/theta, 25 cycles, adversarial barriers and basis switching, plus post-transpile resource audit. | 97.8% fidelity; compiled depth 29; size 48; ops rz/sx/cz/measure/barrier | pass |
| 10 | Key exchange loop | ibm_marrakesh | 100-stage key-shuffling and authentication loop comparing split-complex and standard binary tracks. | Split-complex: 98.4%; standard binary: 98.5% | neutral |
| 11 | Two-qubit ER/EPR-style subspace recovery | ibm_marrakesh | Two-qubit holographic scrambling, inverse recovery, and target payload reconstruction. | 98.9% traversal/recovery rate | pass_as_analogy |
| 12 | Four-qubit macro wormhole simulator | ibm_kingston | Four-qubit expanded macro recovery to target signature 0000. | 97.1% payload reconstruction fidelity | pass_as_analogy |
| 13 | Four-qubit adversarial macro stress | ibm_kingston | 20 adversarial macro-manifold cycles with asynchronous phase barriers and forced physical execution. | 94.2% fidelity; compiled depth 33; size 108 | pass |
| 14 | Dynamic anti-cancellation test | ibm_kingston | Mid-circuit conditional branching designed to prevent compiler identity cancellation. | 82.6% fidelity; compiled depth 14; includes if_else operations | hardest_stress_case |
| 15 | Compiler bridge efficiency benchmark | ibm_kingston | Standard trotterized phase track versus gate-sliced split-complex compiler bridge. | Both tracks 95.0%; 0.0% two-qubit gate savings | neutral |
| 16 | Statistical error-bar validation | ibm_marrakesh | 2,000-shot run with 2,000 bootstrap resampling iterations. | Mean 98.051%; sigma +/-0.313%; 95% CI [97.400%, 98.650%] | pass |
| 17 | QEC scalability net efficiency | ibm_marrakesh | 150-cycle scaled background workload with post-transpile two-qubit pulse-count comparison. | Standard: 2 two-qubit pulses; split-complex: 0; 100.0% fewer reported pulses | pass_with_caveat |
