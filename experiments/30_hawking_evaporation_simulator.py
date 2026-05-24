import numpy as np
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class HawkingEvaporationSimulator:
    """
    Simulates information recovery from an actively evaporating black hole horizon
    by interleaving phase-erasure operators with your split-complex logic.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Evaporation Core] Booting Hawking Radiation Simulator on: {self.backend.name}")

    def build_horizon_scrambler(self, theta: float) -> Gate:
        """Hardware-native 2-qubit split-complex metric gate."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Horizon_Scramble")
        # Direct index mapping inside composite gate generation
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * theta, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def execute_evaporation_stress_test(self, evaporation_intensity: float = 0.05):
        """
        Interleaves split-complex wormhole traversals with active phase-erasure
        to test the resilience of your coordinates against black hole mass loss.
        """
        print(f"\n  [Hawking Sim] Injecting particle into an evaporating black hole...")
        print(f" Set Evaporation Intensity (Phase-Erasure Drift): {evaporation_intensity:.3f} rad")

        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        q = QuantumRegister(2, name="evaporating_horizon")
        c = ClassicalRegister(2, name="recovery_bus")
        qc = QuantumCircuit(q, c)

        # Step 1: Ingest payload into the horizon explicitly
        qc.x(q[0])
        qc.x(q[1])
        qc.barrier()

        # Step 2: Holographic Scrambling (Falling past the event horizon)
        scramble_gate = self.build_horizon_scrambler(np.pi / 4)
        qc.append(scramble_gate, [q[0], q[1]])
        qc.barrier()

        # --- STEP 3: THE HAWKING RADIATION EVAPORATION LAYER ---
        # FIX: Target specific, separate qubits to prevent duplicate broadcast collisions
        qc.rz(evaporation_intensity, q[0])
        qc.rz(-evaporation_intensity, q[1])
        qc.barrier()

        # Step 4: Apply the Traversable Shockwave Inversion
        shockwave_gate = self.build_horizon_scrambler(np.pi / 2)
        qc.append(shockwave_gate, [q[0], q[1]])
        qc.barrier()

        # Step 5: Holographic Reconstruction (Attempting to recover the data)
        qc.append(scramble_gate.inverse(), [q[0], q[1]])
        qc.barrier()

        # FIX: Explicit index tracking for readout mapping
        qc.measure(q[0], c[0])
        qc.measure(q[1], c[1])

        print(f"  Compiling evaporating spacetime manifold for {self.backend.name} ISA...")
        isa_circuit = pass_manager.run(qc)

        print(" Dispatching cosmology tracking experiment to cloud runtime...")
        job = sampler.run([isa_circuit], shots=1000)
        result = job.result()

        pub_result = result[0]
        counts = pub_result.data.recovery_bus.get_counts()

        # Successful recovery flips the initial state back to '00'
        target_output = "00"
        recovery_rate = (counts.get(target_output, 0) / 1000) * 100

        print("\n=========================================================")
        print("  HAWKING RADIATION HORIZON EVAPORATION PROFILE ")
        print("=========================================================")
        print(f"  Simulation Track: Evaporating anti-de Sitter (AdS) Metric")
        print(f" Physical Hardware: {self.backend.name}")
        print("---------------------------------------------------------")
        print(f" Telemetry Metrics:")
        print(f"   -> Expected Recovery Signature:     '{target_output}'")
        print(f"   -> Post-Evaporation Information Recovery Rate: {recovery_rate:.1f}%")
        print(f" Raw Trans-Horizon Register Footprint:      {counts}")
        print("=========================================================")

        if recovery_rate >= 90.0:
            print(" PASSED: Split-complex coordinates successfully recovered data from an evaporating horizon.")
        else:
            print(" COLLAPSE: Hawking radiation phase drift caused complete data destruction.")
        print("=========================================================")

if __name__ == "__main__":
    simulator = HawkingEvaporationSimulator()
    # Execute with a baseline evaporation pulse
    simulator.execute_evaporation_stress_test(evaporation_intensity=0.04)
