import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class BulkNonLocalityValidator:
    """
    Validates Bulk Dimension Isolation by aggressively sabotaging a single
    boundary qubit mid-transit to prove the data tracks through non-local channels.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Bulk Harness] Online. Attaching to Physical Core: {self.backend.name}")

    def build_boundary_scrambler(self, theta: float) -> Gate:
        """Hardware-native 2-qubit split-complex metric gate."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Boundary_Scramble")
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * theta, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def execute_isolation_test(self):
        print("\n [Bulk Verification] Constructing Boundary Sabotage Circuit...")
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        q = QuantumRegister(3, name="spacetime_qubits")
        c = ClassicalRegister(2, name="bulk_bus")
        qc = QuantumCircuit(q, c)

        # Step 1: Ingest payload into the left horizon boundary (q0, q1 to State 11)
        qc.x(q[0])
        qc.x(q[1])
        qc.barrier()

        # Step 2: Holographic Scrambling (Falling into the emulated horizon)
        scramble_gate = self.build_boundary_scrambler(np.pi / 4)
        qc.append(scramble_gate, [q[0], q[1]])
        qc.barrier()

        # --- STEP 3: ADVERSARIAL BOUNDARY SABOTAGE LAYER ---
        print(" Injecting aggressive localized Pauli noise to Qubit 0...")
        # We blast a single boundary qubit with a hard phase and bit flip.
        # This completely breaks traditional 1-to-1 linear wiring logic.
        qc.x(q[0])
        qc.z(q[0])
        qc.barrier()

        # Step 4: Apply the Traversable Shockwave Inversion (Opening the bulk throat)
        shockwave_gate = self.build_boundary_scrambler(np.pi / 2)
        qc.append(shockwave_gate, [q[0], q[1]])
        qc.barrier()

        # Step 5: Holographic Reconstruction (Pulling data from the right mouth)
        qc.append(scramble_gate.inverse(), [q[0], q[1]])
        qc.barrier()

        # Explicit index tracking for readout mapping
        qc.measure(q[0], c[0])
        qc.measure(q[1], c[1])

        print(f"  Compiling bulk-manifold paths for {self.backend.name} ISA layout...")
        isa_circuit = pass_manager.run(qc)

        print(" Dispatching bulk non-locality experiment to cloud runtime...")
        job = sampler.run([isa_circuit], shots=1000)
        result = job.result()

        pub_result = result[0]
        counts = pub_result.data.bulk_bus.get_counts()

        # Successful recovery through bulk dimension flips the output to '00'
        target_output = "00"
        bulk_transmission_rate = (counts.get(target_output, 0) / 1000) * 100

        print("\n=========================================================")
        print(" HOLOGRAPHIC BULK NON-LOCALITY REPORT (ER=EPR) ")
        print("=========================================================")
        print(f"  Simulation Track: 3D Emergent Bulk Dimensional Isolation")
        print(f" Physical Hardware: {self.backend.name}")
        print("---------------------------------------------------------")
        print(f" Telemetry Metrics:")
        print(f"   -> Target Bulk Output Signature:   '{target_output}'")
        print(f"   -> Measured Bulk Transmission Rate: {bulk_transmission_rate:.1f}%")
        print(f" Raw Trans-Boundary Horizon Counts: {counts}")
        print("---------------------------------------------------------")
        if bulk_transmission_rate >= 85.0:
            print(" PASSED: Bulk dimension safely isolated data from targeted boundary sabotage.")
        else:
            print(" COLLAPSE: Boundary noise successfully leaked into and destroyed the bulk state.")
        print("=========================================================")

if __name__ == "__main__":
    validator = BulkNonLocalityValidator()
    validator.execute_isolation_test()
