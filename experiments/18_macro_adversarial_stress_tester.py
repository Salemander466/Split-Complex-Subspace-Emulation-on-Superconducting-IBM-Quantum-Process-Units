import numpy as np
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class MacroAdversarialStressTester:
    """
    Adversarial verification rig designed to stress-test 4-qubit macro-wormholes.
    Blocks compiler shortcuts via asynchronous phase barriers and audits QPU metrics.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Stress Rig] Online. Attaching to Physical Core: {self.backend.name}")

    def build_metric_gate(self, theta: float) -> Gate:
        """Hardware-native 2-qubit decomposition block."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Metric_Layer")
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * theta, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def execute_destructive_macro_test(self, stress_cycles: int = 20):
        """
        Forces physical gate execution over 20 layered macro-cycles (80+ gates)
        by interleaving un-optimizable phase and basis-switching barriers.
        """
        base_theta = np.pi / 4
        print(f" [Stress Config] Launching {stress_cycles} Adversarial Multi-Manifold Cycles...")

        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        q = QuantumRegister(4, name="macro_spacetime")
        c = ClassicalRegister(4, name="macro_throat")
        qc = QuantumCircuit(q, c)

        # Ingestion Payload (State 1111)
        qc.x(q[0])
        qc.x(q[1])
        qc.x(q[2])
        qc.x(q[3])
        qc.barrier()

        # Tracking arrays to reverse the precise randomized trajectories manually
        angle_perturbations = []
        rz_barriers = []
        ry_basis_swaps = []

        # --- PHASE 1: ADVERSARIAL MULTI-MANIFOLD SCRAMBLING ---
        print(" Injecting asynchronous phase barriers across the macro-manifold...")
        for _ in range(stress_cycles):
            eps = random.uniform(-0.01, 0.01)
            angle_perturbations.append(eps)

            # FIX: Explicit index tracking separating the two independent spatial horizons
            scramble_gate = self.build_metric_gate(base_theta + eps)
            qc.append(scramble_gate, [q[0], q[1]])
            qc.append(scramble_gate, [q[2], q[3]])

            # Interleave independent random RZ and RY barriers to blind the compiler
            rz_p = random.uniform(-0.02, 0.02)
            ry_p = random.uniform(-0.01, 0.01)
            rz_barriers.append(rz_p)
            ry_basis_swaps.append(ry_p)

            # FIX: Apply asynchronously across distinct INDIVIDUAL qubits to break compiler symmetry
            qc.rz(rz_p, q[0])
            qc.ry(ry_p, q[1])
            qc.rz(rz_p, q[2])
            qc.ry(ry_p, q[3])

        qc.barrier()

        # --- PHASE 2: SUSTAINED STABILIZATION SHOCKWAVE ---
        shockwave_gate = self.build_metric_gate(np.pi / 2)
        qc.append(shockwave_gate, [q[0], q[1]])
        qc.append(shockwave_gate, [q[2], q[3]])
        qc.barrier()

        # --- PHASE 3: ADVERSARIAL UN-SCRAMBLING ---
        print(" Deploying adversarial inverse phase reconstruction sequence...")
        for eps, rz_p, ry_p in zip(reversed(angle_perturbations), reversed(rz_barriers), reversed(ry_basis_swaps)):
            qc.ry(-ry_p, q[3])
            qc.rz(-rz_p, q[2])
            qc.ry(-ry_p, q[1])
            qc.rz(-rz_p, q[0])

            unscramble_gate = self.build_metric_gate(-(base_theta + eps))
            qc.append(unscramble_gate, [q[0], q[1]])
            qc.append(unscramble_gate, [q[2], q[3]])

        qc.barrier()

        # FIX: Map measurements to specific indices on the classical register
        qc.measure(q[0], c[0])
        qc.measure(q[1], c[1])
        qc.measure(q[2], c[2])
        qc.measure(q[3], c[3])

        # Transpilation Pass Audit
        print("  Running aggressive compilation and circuit layout optimizations...")
        isa_circuit = pass_manager.run(qc)

        print("\n=========================================================")
        print(" POST-TRANSPILE ADVERSARIAL RESOURCE AUDIT ")
        print("=========================================================")
        print(f" Native Operations Map: {isa_circuit.count_ops()}")
        print(f" Compiled Hardware Depth: {isa_circuit.depth()}")
        print(f" Structural Circuit Size: {isa_circuit.size()}")
        print("=========================================================\n")

        print(f" Transmitting payload pipeline to {self.backend.name} queue...")
        job = sampler.run([isa_circuit], shots=1000)
        result = job.result()

        pub_result = result[0]
        counts = pub_result.data.macro_throat.get_counts()

        target_output = "0000"
        traversal_fidelity = (counts.get(target_output, 0) / 1000) * 100

        print("=========================================================")
        print(" REAL-WORLD ADVERSARIAL MACRO-TELEMETRY")
        print("=========================================================")
        print(f" Target Macro Signal Signature:   '{target_output}'")
        print(f" Protected Macro-Throat Fidelity: {traversal_fidelity:.1f}%")
        print(f" Raw Hardware Multi-Manifold Counts: {counts}")
        print("=========================================================")

if __name__ == "__main__":
    tester = MacroAdversarialStressTester()
    tester.execute_destructive_macro_test(stress_cycles=20)
