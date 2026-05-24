import numpy as np
import json
import math
from collections import defaultdict
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from google.colab import userdata


class SplitComplexBreakthroughValidationSuite:
    """
    Goal:
    Test whether the split-complex mapped architecture shows either:

    1. Simulator-resistant behavior:
       Hardware result deviates materially from exact same-circuit statevector prediction.

    2. Baseline advantage:
       Split-complex recovery significantly outperforms matched baseline circuits.

    This does not prove new physics by itself.
    It creates the strongest next validation dataset.
    """

    def __init__(
        self,
        backend_name=None,
        shots=10000,
        optimization_level=3,
        depths=(5, 10, 25, 50),
        theta_degrees=(15, 30, 45, 60, 75, 90),
        seed=166,
    ):
        self.token = userdata.get("ibm2")
        if not self.token:
            raise ValueError("Missing IBM token in Colab secrets under key: ibm")

        self.service = QiskitRuntimeService(
            channel="ibm_quantum_platform",
            token=self.token
        )

        if backend_name is None:
            self.backend = self.service.least_busy(
                simulator=False,
                operational=True
            )
        else:
            self.backend = self.service.backend(backend_name)

        self.shots = int(shots)
        self.optimization_level = int(optimization_level)
        self.depths = list(depths)
        self.theta_degrees = list(theta_degrees)
        self.seed = int(seed)
        self.rng = np.random.default_rng(seed)

        print("Backend:", self.backend.name)
        print("Shots:", self.shots)
        print("Optimization level:", self.optimization_level)
        print("Depths:", self.depths)
        print("Theta degrees:", self.theta_degrees)

    def split_gate(self, qc, q0, q1, theta):
        qc.cx(q0, q1)
        qc.ry(2.0 * theta, q0)
        qc.cx(q0, q1)

    def inverse_split_gate(self, qc, q0, q1, theta):
        qc.cx(q0, q1)
        qc.ry(-2.0 * theta, q0)
        qc.cx(q0, q1)

    def add_ant_cancel(self, qc, q, scale=0.015):
        e0 = float(self.rng.uniform(-scale, scale))
        e1 = float(self.rng.uniform(-scale, scale))
        e2 = float(self.rng.uniform(-scale, scale))
        qc.rz(e0, q[0])
        qc.ry(e1, q[1])
        qc.sx(q[0])
        qc.rz(e2, q[1])

    def build_split_complex_recovery(self, theta, depth, target_bit=1):
        q = QuantumRegister(2, "q")
        c = ClassicalRegister(2, "c")
        qc = QuantumCircuit(q, c, name="split_complex_recovery")

        if target_bit == 1:
            qc.x(q[0])
            qc.x(q[1])

        for _ in range(depth):
            self.split_gate(qc, q[0], q[1], theta)
            self.add_ant_cancel(qc, q)

        qc.barrier()

        for _ in range(depth):
            self.add_ant_cancel(qc, q)
            self.inverse_split_gate(qc, q[0], q[1], theta)

        qc.measure(q, c)
        return qc

    def build_identity_reversible_baseline(self, theta, depth, target_bit=1):
        q = QuantumRegister(2, "q")
        c = ClassicalRegister(2, "c")
        qc = QuantumCircuit(q, c, name="identity_reversible_baseline")

        if target_bit == 1:
            qc.x(q[0])
            qc.x(q[1])

        for _ in range(depth):
            qc.ry(theta, q[0])
            qc.ry(-theta, q[0])
            qc.rz(theta, q[1])
            qc.rz(-theta, q[1])
            self.add_ant_cancel(qc, q)

        qc.barrier()

        for _ in range(depth):
            self.add_ant_cancel(qc, q)
            qc.rz(theta, q[1])
            qc.rz(-theta, q[1])
            qc.ry(theta, q[0])
            qc.ry(-theta, q[0])

        qc.measure(q, c)
        return qc

    def build_random_matched_baseline(self, theta, depth, target_bit=1):
        q = QuantumRegister(2, "q")
        c = ClassicalRegister(2, "c")
        qc = QuantumCircuit(q, c, name="random_matched_baseline")

        if target_bit == 1:
            qc.x(q[0])
            qc.x(q[1])

        for _ in range(depth * 2):
            a = float(self.rng.uniform(-np.pi, np.pi))
            b = float(self.rng.uniform(-np.pi, np.pi))
            qc.cx(q[0], q[1])
            qc.ry(a, q[0])
            qc.rz(b, q[1])
            qc.cx(q[0], q[1])

        qc.measure(q, c)
        return qc

    def build_standard_phase_baseline(self, theta, depth, target_bit=1):
        q = QuantumRegister(2, "q")
        c = ClassicalRegister(2, "c")
        qc = QuantumCircuit(q, c, name="standard_phase_baseline")

        if target_bit == 1:
            qc.x(q[0])
            qc.x(q[1])

        for _ in range(depth):
            qc.rz(theta, q[0])
            qc.ry(theta / 2.0, q[1])
            qc.cx(q[0], q[1])
            qc.rz(-theta, q[0])
            qc.cx(q[0], q[1])
            self.add_ant_cancel(qc, q)

        qc.measure(q, c)
        return qc

    def ideal_probs_from_circuit(self, qc):
        unitary_part = qc.remove_final_measurements(inplace=False)
        try:
            sv = Statevector.from_instruction(unitary_part)
            probs = sv.probabilities_dict()
            return {k: float(probs.get(k, 0.0)) for k in ["00", "01", "10", "11"]}
        except Exception as exc:
            return {
                "error": str(exc),
                "00": None,
                "01": None,
                "10": None,
                "11": None,
            }

    def normalize_counts(self, counts):
        total = sum(counts.values())
        if total == 0:
            return {k: 0.0 for k in ["00", "01", "10", "11"]}
        return {k: counts.get(k, 0) / total for k in ["00", "01", "10", "11"]}

    def total_variation_distance(self, p, q):
        if p.get("00") is None or q.get("00") is None:
            return None
        return 0.5 * sum(abs(p[k] - q[k]) for k in ["00", "01", "10", "11"])

    def target_fidelity(self, probs, target_bit=1):
        target = "11" if target_bit == 1 else "00"
        return probs.get(target, 0.0)

    def two_proportion_z(self, p1, p2):
        n = self.shots
        se = math.sqrt(
            max(1e-12, p1 * (1.0 - p1) / n) +
            max(1e-12, p2 * (1.0 - p2) / n)
        )
        return (p1 - p2) / se

    def audit_circuit(self, qc):
        return {
            "depth": qc.depth(),
            "size": qc.size(),
            "ops": dict(qc.count_ops())
        }

    def run(self):
        builders = {
            "split_complex_recovery": self.build_split_complex_recovery,
            "identity_reversible_baseline": self.build_identity_reversible_baseline,
            "standard_phase_baseline": self.build_standard_phase_baseline,
            "random_matched_baseline": self.build_random_matched_baseline,
        }

        raw_circuits = []
        metadata = []

        for depth in self.depths:
            for theta_deg in self.theta_degrees:
                theta = np.deg2rad(theta_deg)
                for name, builder in builders.items():
                    qc = builder(theta=theta, depth=depth, target_bit=1)
                    raw_circuits.append(qc)
                    metadata.append({
                        "model": name,
                        "depth_parameter": depth,
                        "theta_deg": theta_deg,
                        "target_bit": 1
                    })

        print("Raw circuits:", len(raw_circuits))

        pass_manager = generate_preset_pass_manager(
            backend=self.backend,
            optimization_level=self.optimization_level
        )

        isa_circuits = []
        compiled_audits = []
        ideal_probs = []

        print("Transpiling and computing exact statevector predictions...")
        for qc in raw_circuits:
            isa = pass_manager.run(qc)
            isa_circuits.append(isa)
            compiled_audits.append(self.audit_circuit(isa))
            ideal_probs.append(self.ideal_probs_from_circuit(isa))

        print("Submitting to backend:", self.backend.name)
        sampler = SamplerV2(self.backend)
        job = sampler.run(isa_circuits, shots=self.shots)

        print("Job ID:", job.job_id())
        result = job.result()

        rows = []

        for i, meta in enumerate(metadata):
            counts = result[i].data.c.get_counts()
            hardware_probs = self.normalize_counts(counts)
            ideal = ideal_probs[i]

            row = {
                "backend": self.backend.name,
                "job_id": job.job_id(),
                "model": meta["model"],
                "depth_parameter": meta["depth_parameter"],
                "theta_deg": meta["theta_deg"],
                "shots": self.shots,
                "target_bit": meta["target_bit"],
                "raw_counts": counts,
                "hardware_probs": hardware_probs,
                "ideal_statevector_probs": ideal,
                "hardware_target_fidelity": self.target_fidelity(hardware_probs, meta["target_bit"]),
                "ideal_target_fidelity": self.target_fidelity(ideal, meta["target_bit"]) if ideal.get("00") is not None else None,
                "hardware_vs_ideal_tvd": self.total_variation_distance(hardware_probs, ideal),
                "compiled_audit": compiled_audits[i],
            }

            rows.append(row)

        comparisons = self.make_comparisons(rows)

        output = {
            "test_name": "Breakthrough Validation Suite: Simulator Residual and Baseline Advantage",
            "backend": self.backend.name,
            "shots": self.shots,
            "optimization_level": self.optimization_level,
            "depths": self.depths,
            "theta_degrees": self.theta_degrees,
            "rows": rows,
            "comparisons": comparisons,
            "interpretation_rules": {
                "simulator_resistant_screen": (
                    "Potentially interesting if split_complex_recovery has large hardware_vs_ideal_tvd "
                    "that repeats across backends while baselines do not."
                ),
                "baseline_advantage_screen": (
                    "Strong if split_complex_recovery beats every matched baseline by more than "
                    "10 percentage points and more than 5 standard errors across most theta-depth settings."
                ),
                "new_physics_warning": (
                    "This suite alone does not prove new physics. Same-circuit residuals must be repeated "
                    "with noise models, readout mitigation, and independent backends."
                )
            }
        }

        filename = "breakthrough_validation_suite_results.json"
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)

        self.print_report(rows, comparisons, filename)
        return output

    def make_comparisons(self, rows):
        grouped = defaultdict(dict)

        for r in rows:
            key = (r["depth_parameter"], r["theta_deg"])
            grouped[key][r["model"]] = r

        comparisons = []

        for key, group in grouped.items():
            depth, theta_deg = key
            split = group.get("split_complex_recovery")
            if split is None:
                continue

            split_fid = split["hardware_target_fidelity"]

            for baseline_name in [
                "identity_reversible_baseline",
                "standard_phase_baseline",
                "random_matched_baseline",
            ]:
                baseline = group.get(baseline_name)
                if baseline is None:
                    continue

                base_fid = baseline["hardware_target_fidelity"]
                delta = split_fid - base_fid
                z = self.two_proportion_z(split_fid, base_fid)

                comparisons.append({
                    "depth_parameter": depth,
                    "theta_deg": theta_deg,
                    "split_model": "split_complex_recovery",
                    "baseline_model": baseline_name,
                    "split_fidelity": split_fid,
                    "baseline_fidelity": base_fid,
                    "delta_fidelity": delta,
                    "z_score": z,
                    "split_hardware_vs_ideal_tvd": split["hardware_vs_ideal_tvd"],
                    "baseline_hardware_vs_ideal_tvd": baseline["hardware_vs_ideal_tvd"],
                })

        return comparisons

    def print_report(self, rows, comparisons, filename):
        print("\n============================================================")
        print("BREAKTHROUGH VALIDATION SUITE REPORT")
        print("============================================================")
        print("Backend:", self.backend.name)
        print("Shots:", self.shots)
        print("Saved JSON:", filename)
        print("------------------------------------------------------------")

        split_rows = [r for r in rows if r["model"] == "split_complex_recovery"]
        avg_split_fid = np.mean([r["hardware_target_fidelity"] for r in split_rows])
        avg_split_tvd = np.mean([r["hardware_vs_ideal_tvd"] for r in split_rows if r["hardware_vs_ideal_tvd"] is not None])

        print("Average split-complex hardware target fidelity:", round(float(avg_split_fid), 4))
        print("Average split-complex hardware-vs-ideal TVD:", round(float(avg_split_tvd), 4))

        print("\nTop baseline advantages:")
        top_adv = sorted(comparisons, key=lambda x: x["z_score"], reverse=True)[:10]
        for c in top_adv:
            print(
                f"depth={c['depth_parameter']:>3} theta={c['theta_deg']:>3} "
                f"vs={c['baseline_model']} "
                f"split={c['split_fidelity']:.4f} "
                f"base={c['baseline_fidelity']:.4f} "
                f"delta={c['delta_fidelity']:+.4f} "
                f"z={c['z_score']:+.2f}"
            )

        print("\nLargest hardware-vs-statevector residuals:")
        residuals = [
            r for r in rows
            if r["hardware_vs_ideal_tvd"] is not None
        ]
        residuals = sorted(residuals, key=lambda r: r["hardware_vs_ideal_tvd"], reverse=True)[:10]
        for r in residuals:
            print(
                f"{r['model']} depth={r['depth_parameter']} theta={r['theta_deg']} "
                f"TVD={r['hardware_vs_ideal_tvd']:.4f} "
                f"hardware_fid={r['hardware_target_fidelity']:.4f} "
                f"ideal_fid={r['ideal_target_fidelity']:.4f} "
                f"ops={r['compiled_audit']['ops']}"
            )

        print("\nDecision standard:")
        print("1. Baseline advantage: split-complex should beat all baselines by >10 percentage points and >5 z-score.")
        print("2. Simulator resistance: split-complex should show repeated hardware-vs-statevector residuals not seen in baselines.")
        print("3. Physics claim: not valid until repeated across backends with noise models and readout mitigation.")


suite = SplitComplexBreakthroughValidationSuite(
    backend_name=None,          # or "ibm_marrakesh", "ibm_kingston", "ibm_fez"
    shots=10000,
    optimization_level=3,
    depths=(5, 10, 25, 50),
    theta_degrees=(15, 30, 45, 60, 75, 90),
    seed=166
)

breakthrough_results = suite.run()