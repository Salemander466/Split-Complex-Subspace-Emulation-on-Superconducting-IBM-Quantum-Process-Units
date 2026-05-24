# Hyperbolic Subspace Quantum Cryptography

Production-grade validation repository for mapped split-complex logical emulation inside standard complex-valued quantum circuits.

This repository packages the notebook-derived experiments into reproducible source files, a result catalog, and documentation suitable for scientific review. The project does not claim new physics, physical wormholes, literal quantum error correction replacement, or physical pulse compression without backend-native schedule evidence. The claim is narrower and stronger: these experiments evaluate whether a structured reversible mapping can recover logical payloads reliably on current IBM superconducting QPUs.

## Core result

Across the formal 17-test validation set, the strongest reproducible hardware results include:

- 98.051% mean fidelity with a 95% confidence interval of 97.400% to 98.650%.
- 97.8% adversarial randomized recovery with post-transpile resource audit.
- 97.8% recovery at 100,000 nominal programmed forward/reverse gate-pair depth.
- 97.2% recovery under active neighboring-qubit interference.

The hardest stress case is the dynamic anti-cancellation test at 82.6%. This is important because it prevents the compiler from reducing the experiment into a trivial identity circuit.

## Repository layout

```text
src/hscq/                         Core package utilities
experiments/                       Notebook-derived hardware experiment scripts
results/VALIDATION_TABLE.md        Formal 17-test result table
results/validation_results.json    Machine-readable results catalog
docs/                              Scientific notes and licensing policy
notebooks/Quantum_full.ipynb       Original notebook evidence archive
tests/                             Local unit tests for circuit builders
```

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Local circuit inspection

```bash
hscq-build loopback --depth 8 --bit 1
hscq-build crosstalk
hscq-build adversarial --depth 25 --bit 0
```

These commands build circuits and report local circuit structure. They do not submit IBM Quantum jobs. Hardware execution requires IBM Quantum credentials and the scripts in `experiments/`.

## Reproduction protocol

1. Create an IBM Quantum account.
2. Set `IBM_QUANTUM_TOKEN` in the environment.
3. Install the project dependencies.
4. Run the desired script in `experiments/`.
5. Record backend name, shots, raw counts, post-transpile operations, compiled depth, structural size, and scheduled duration when available.
6. Compare results against `results/validation_results.json`.

## Scientific boundaries

This repository demonstrates mapped circuit behavior under real QPU execution. It does not demonstrate fault-tolerant computation, literal QEC replacement, new particles, physical hyperbolic quantum states, or spacetime engineering. Holographic and gravitational terminology is used as an analogy for reversible scrambling and recovery protocols.

## License

Dual-license model:

- Public license: AGPL-3.0-or-later.
- Commercial license: available separately for proprietary, hosted, closed-source, enterprise, or revenue-generating use. See `COMMERCIAL_LICENSE.md`.

## Latest Research Notes

The current phase-linked conceptual report is available at:

- `docs/UPDATED_REPORT_NOTES_3_CONCEPTUAL_PHASE_MAPPING.md`
- `results/conceptual_phase_mapping.json`

These files link each experimental phase to the relevant test results, conceptual theories, challenged assumptions, caveats, APA7 references, and BibTeX citations.


## Latest QELU v6.0 and Breakthrough Validation Results

This release adds:

- `experiments/qelu_monolithic_geometry_miner.py`
- `experiments/qelu_v6_advanced_analytics.py`
- `experiments/breakthrough_validation_suite.py`
- `docs/LATEST_QELU_AND_BREAKTHROUGH_RESULTS.md`
- `data/results/latest_qelu_and_breakthrough_results.json`

Latest interpretation: QELU is locally robust but globally decoder-limited; cross-backend breakthrough validation shows strong selected-regime baseline advantage on ibm_fez and ibm_marrakesh. Simulator resistance, new physics, and Born-rule violation remain unproven.
