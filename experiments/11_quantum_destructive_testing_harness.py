import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class QuantumDestructiveTestingHarness:
    """
    An automated hardware stress testing rig designed to continuously scale
    circuit depth to physically locate the exact failure limits of the protocol.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Destructive Harness] Online. Locked on Target Core: {self.backend.name}")

    def build_emulation_gate(self, theta: float, inverse: bool = False) -> Gate:
        """Hardware-native 2-qubit decomposition sequence."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Split_Complex_Gate")
        angle = -theta if inverse else theta
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * angle, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def find_absolute_physical_limits(self, target_bit: int = 1, theta: float = np.pi/4):
        # Testing specific steps to evaluate rapid accumulation of phase noise
        depth_testing_steps = [1000, 10000, 100000]

        print(f" Beginning Stress-To-Failure loop across {len(depth_testing_steps)} hardware increments...")

        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)
        circuits = []

        for d in depth_testing_steps:
            q = QuantumRegister(2, name="squbit")
            c = ClassicalRegister(2, name="secure_bus")
            qc = QuantumCircuit(q, c)

            # Data Ingestion: Explicit index allocation
            if target_bit == 1:
                qc.x(q[0])
                qc.x(q[1])

            f_gate = self.build_emulation_gate(theta, inverse=False)
            r_gate = self.build_emulation_gate(theta, inverse=True)

            # Iteratively stack the forward gates directly into a long chain
            for _ in range(d):
                qc.append(f_gate, [q[0], q[1]])
            qc.barrier()

            # Iteratively stack the corresponding decryption/reverse passes
            for _ in range(d):
                qc.append(r_gate, [q[0], q[1]])
            qc.barrier()

            # Readout mapping using individual indices
            qc.measure(q[0], c[0])
            qc.measure(q[1], c[1])
            circuits.append(pass_manager.run(qc))

        print(f" Dispatching destructive payload pipeline to {self.backend.name} cloud queue...")
        job = sampler.run(circuits, shots=1000)
        result = job.result()

        print("\n=========================================================")
        print(" CRITICAL STRESS-TO-FAILURE DIAGNOSTIC RESULTS ")
        print("=========================================================")

        target_str = "11" if target_bit == 1 else "00"
        security_breached = False
        operational_failed = False

        for i, d in enumerate(depth_testing_steps):
            counts = result[i].data.secure_bus.get_counts()
            fidelity = (counts.get(target_str, 0) / 1000) * 100
            leakage = 100.0 - fidelity

            status = " SECURE"
            if fidelity < 95.0 and not security_breached:
                status = " SECURITY THRESHOLD BREACHED (<95% Fidelity)"
                security_breached = True
            elif fidelity <= 50.0:
                status = " OPERATIONAL FAILURE BLOCK (Data Fully Dissolved)"
                operational_failed = True
            elif security_breached:
                status = " UNSECURE TRANSIT LAYER"

            print(f" Depth: {d:2d} Pairs ({d*2:3d} Physical Gates) | Fidelity: {fidelity:5.1f}% | Leakage: {leakage:5.1f}% | [{status}]")
            print(f"   Raw Hardware Bitstring Footprint: {counts}")
        print("=========================================================")

# =====================================================================
# RUNNING THE DESTRUCTIVE EVALUATION LOOP
# =====================================================================
if __name__ == "__main__":
    harness = QuantumDestructiveTestingHarness()
    harness.find_absolute_physical_limits(target_bit=1, theta=np.pi/4)
