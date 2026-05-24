import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class GravitationalTimeDelaySimulator:
    """
    Simulates Shapiro time-delay inside a holographic traversable wormhole
    by stacking sequential, competing positive and negative energy shockwave gates.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Gravitational Core] Booting Multi-Shockwave Engine on: {self.backend.name}")

    def build_metric_gate(self, theta: float, name="Metric_Layer") -> Gate:
        """Hardware-native 2-qubit split-complex metric gate."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name=name)
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * theta, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def execute_time_delay_benchmark(self, bottleneck_intensity: float = np.pi/12):
        """
        Executes back-to-back competing shockwave transformations to measure
        the resulting phase-shift delay on the physical QPU.
        """
        print(f"\n [Shapiro Sim] Initializing Multi-Shockwave Spacetime Bottleneck...")
        print(f" Set Bottleneck Intensity (Positive Shockwave Angle): {np.degrees(bottleneck_intensity):.1f}")

        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        q = QuantumRegister(2, name="spacetime_qubits")
        c = ClassicalRegister(2, name="telemetry_bus")
        qc = QuantumCircuit(q, c)

        # Step 1: Ingest payload into the horizon (State 11)
        qc.x(q[0])
        qc.x(q[1])
        qc.barrier()

        # Step 2: Holographic Scrambling
        scramble_gate = self.build_metric_gate(np.pi / 4, name="Scramble")
        qc.append(scramble_gate, [q[0], q[1]])
        qc.barrier()

        # --- STEP 3: THE COMPETING MULTI-SHOCKWAVE BLOCK ---
        # 1. Inject Positive-Energy Shockwave (Clamps the throat, creating the time-delay)
        positive_shockwave = self.build_metric_gate(bottleneck_intensity, name="Pos_Shockwave")
        qc.append(positive_shockwave, [q[0], q[1]])

        # 2. Inject Negative-Energy Shockwave (Forces the throat open against the bottleneck)
        negative_shockwave = self.build_metric_gate(np.pi / 2, name="Neg_Shockwave")
        qc.append(negative_shockwave, [q[0], q[1]])
        qc.barrier()

        # Step 4: Holographic Reconstruction (Unwinding the initial trajectory)
        qc.append(scramble_gate.inverse(), [q[0], q[1]])
        qc.barrier()

        # Readout mapping using individual indices
        qc.measure(q[0], c[0])
        qc.measure(q[1], c[1])

        print(f"  Compiling multi-shockwave geometry for {self.backend.name} ISA...")
        isa_circuit = pass_manager.run(qc)

        print(" Dispatching Shapiro time-delay experiment to cloud runtime...")
        job = sampler.run([isa_circuit], shots=1000)
        result = job.result()

        pub_result = result[0]
        counts = pub_result.data.telemetry_bus.get_counts()

        # Due to the positive bottleneck shift, the target recovery state is modified.
        # The math dictates the signal delays and projects cleanly onto the '00' flipped signature.
        target_output = "00"
        traversal_accuracy = (counts.get(target_output, 0) / 1000) * 100

        print("\n=========================================================")
        print(" SHAPIRO TIME-DELAY MULTI-SHOCKWAVE PROFILE ")
        print("=========================================================")
        print(f"  Simulation Track: Curved 2D AdS Metric Back-Reaction")
        print(f" Physical Hardware: {self.backend.name}")
        print("---------------------------------------------------------")
        print(f" Telemetry Metrics:")
        print(f"   -> Target Delayed Signature:        '{target_output}'")
        print(f"   -> Measured Phase-Tracking Accuracy: {traversal_accuracy:.1f}%")
        print(f" Raw Trans-Bridge Metric Register:   {counts}")
        print("---------------------------------------------------------")
        if traversal_accuracy >= 90.0:
            print(" STATUS: PASSED. QVM successfully mapped continuous gravitational time-delay metrics.")
        else:
            print(" STATUS: FAILED. Phase-blurring noise overwhelmed the bottleneck tracking.")
        print("=========================================================")

if __name__ == "__main__":
    simulator = GravitationalTimeDelaySimulator()
    simulator.execute_time_delay_benchmark(bottleneck_intensity=np.pi/12) # 15-degree positive delay block
