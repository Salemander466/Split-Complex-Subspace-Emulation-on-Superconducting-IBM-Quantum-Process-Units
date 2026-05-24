import numpy as np
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class AdversarialQECCompressionTester:
    """
    An adversarial verification suite designed to stress-test split-complex emulations.
    Blocks compiler optimization via dynamic phase barriers and audits physical QPU footprints.
    """
    def __init__(self, target_backend_name=None):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)

        if target_backend_name:
            self.backend = self.service.backend(target_backend_name)
        else:
            self.backend = self.service.least_busy(simulator=False, operational=True)

        print(f"\n [Harness] System Active. Locked on Target Core: {self.backend.name}")

    def build_emulation_gate(self, theta: float, name="Split_Complex_Gate") -> Gate:
        """Hardware-native 2-qubit decomposition sequence."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name=name)
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * theta, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def execute_adversarial_benchmark(self, qec_loops: int = 100):
        """
        Executes an anti-cancellation stress-test over randomized payloads,
        forcing physical execution and auditing post-transpilation primitives.
        """
        target_bit = random.choice([0, 1])
        base_theta = random.uniform(np.pi/12, np.pi/2)

        print(f" [Randomized Ingestion] Target Bit: {target_bit} | Base Theta: {np.degrees(base_theta):.1f} | Cycles: {qec_loops}")

        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        q_comp = QuantumRegister(2, name="squbit")
        c_comp = ClassicalRegister(2, name="bus_comp")
        qc_comp = QuantumCircuit(q_comp, c_comp)

        if target_bit == 1:
            qc_comp.x(q_comp[0])
            qc_comp.x(q_comp[1])

        applied_perturbations = []
        interleaved_phases = []
        basis_swaps = []

        print(" Injecting adversarial noise barriers and basis-switching entanglers...")
        for _ in range(qec_loops):
            # Anti-Cancellation Step 1: Angle perturbation
            epsilon = random.uniform(-0.01, 0.01)
            f_theta = base_theta + epsilon
            applied_perturbations.append(epsilon)

            f_gate = self.build_emulation_gate(f_theta, name="F_Gate")
            qc_comp.append(f_gate, [q_comp[0], q_comp[1]])

            # Anti-Cancellation Step 2: Random RZ phase barrier injection
            rz_phase = random.uniform(-0.02, 0.02)
            interleaved_phases.append(rz_phase)
            qc_comp.rz(rz_phase, q_comp[0])

            # ADVERSARIAL UPGRADE: Non-local basis rotator to destroy analytical reduction loops
            b_rotation = random.uniform(-0.01, 0.01)
            basis_swaps.append(b_rotation)
            qc_comp.ry(b_rotation, q_comp[1])

        qc_comp.barrier()

        print(" Deploying inverse phase reconstruction sequence...")
        # Unwind everything in strict mathematical reverse order to protect information recovery
        for epsilon, rz_phase, b_rotation in zip(reversed(applied_perturbations), reversed(interleaved_phases), reversed(basis_swaps)):
            qc_comp.ry(-b_rotation, q_comp[1])
            qc_comp.rz(-rz_phase, q_comp[0])

            r_theta = -(base_theta + epsilon)
            r_gate = self.build_emulation_gate(r_theta, name="R_Gate")
            qc_comp.append(r_gate, [q_comp[0], q_comp[1]])

        qc_comp.measure(q_comp[0], c_comp[0])
        qc_comp.measure(q_comp[1], c_comp[1])

        print("  Running aggressive compilation passes...")
        isa_circuit = pass_manager.run(qc_comp)

        print("\n=========================================================")
        print(" POST-TRANSPILE PHYSICAL RESOURCE AUDIT ")
        print("=========================================================")
        print(f" Native Operations Map: {isa_circuit.count_ops()}")
        print(f" Compiled Hardware Depth: {isa_circuit.depth()}")
        print(f" Structural Circuit Size: {isa_circuit.size()}")
        print("=========================================================\n")

        print(f" Transmitting payload to {self.backend.name} cluster...")
        job = sampler.run([isa_circuit], shots=1000)
        result = job.result()

        # FIX: Explicit index matching targeting PubResults arrays natively
        pub_result = result[0]
        counts = pub_result.data.bus_comp.get_counts()

        target_state_str = "11" if target_bit == 1 else "00"
        fidelity = (counts.get(target_state_str, 0) / 1000) * 100

        print("=========================================================")
        print(" REAL-WORLD ADVERSARIAL TELEMETRY OUTPUT")
        print("=========================================================")
        print(f" Expected Recovery Target State: '{target_state_str}'")
        print(f" Verified Subspace Emulation Fidelity: {fidelity:.1f}%")
        print(f" Raw Hardware Register Fingerprint: {counts}")
        print("=========================================================")

        return {
            "backend": self.backend.name,
            "depth": isa_circuit.depth(),
            "fidelity": fidelity
        }

if __name__ == "__main__":
    print("--- Initializing Multi-Backend Adversarial Validation Suite ---")

    # Run across your operational backends
    target_backends = ["ibm_marrakesh", "ibm_fez"]
    artifacts_vault = []

    for backend_name in target_backends:
        try:
            tester = AdversarialQECCompressionTester(target_backend_name=backend_name)
            tester.execute_adversarial_benchmark(qec_loops=25)  # Balanced loop scale for high-stress depth evaluation
        except Exception as e:
            print(f" Could not execute on backend {backend_name}. Error: {str(e)}")
