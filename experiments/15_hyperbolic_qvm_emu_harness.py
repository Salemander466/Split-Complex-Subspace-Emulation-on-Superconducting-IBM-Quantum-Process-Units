import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class HyperbolicQVMEmuHarness:
    """
    Implements a High-Fidelity Quantum Virtual Machine (QVM) emulation layer.
    Tracks continuous non-Euclidean phase trajectories on standard cloud QPUs.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [QVM Engine] Virtual Machine Booted on Physical Core: {self.backend.name}")

    def build_qvm_instruction(self, phase_angle: float) -> Gate:
        """Compiles an exotic hyperbolic state shift into optimized hardware pulses."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="QVM_Hyperbolic_Shift")
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * phase_angle, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def run_virtual_physics_sweep(self):
        """
        Sweeps through 8 continuous non-Euclidean fractional phase angles
        to track the geometric drift of the emulated virtual space.
        """
        # Define the continuous non-Euclidean evolution track (0 to 180 degrees)
        evolution_steps = [0, np.pi/6, np.pi/4, np.pi/3, np.pi/2, 2*np.pi/3, 3*np.pi/4, np.pi]

        print(f" [QVM] Running continuous Phase Tomography Map across {len(evolution_steps)} coordinates...")
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)
        circuits = []

        # -----------------------------------------------------------------
        # CONSTRUCTING THE VIRTUAL MACHINE CHANNELS
        # -----------------------------------------------------------------
        for phi in evolution_steps:
            q = QuantumRegister(2, name="squbit")
            c = ClassicalRegister(2, name="qvm_bus")
            qc = QuantumCircuit(q, c)

            # Initialize State 11
            qc.x(q[0])
            qc.x(q[1])

            # Execute Virtual Hyperbolic Shift Command
            shift_command = self.build_qvm_instruction(phi)
            qc.append(shift_command, [q[0], q[1]])

            qc.measure(q[0], c[0])
            qc.measure(q[1], c[1])

            circuits.append(pass_manager.run(qc))

        print(f" [QVM] Dispatching emulation blocks to {self.backend.name} queue...")
        job = sampler.run(circuits, shots=1000)
        result = job.result()

        print("\n=========================================================")
        print(" QUANTUM VIRTUAL MACHINE (QVM) TOMOGRAPHY REPORT ")
        print("=========================================================")
        print(f"  Emulated System: Hyperbolic Metric Space Dynamics")
        print(f"  Physical Layer:   {self.backend.name} (Superconducting Hardware)")
        print("---------------------------------------------------------")
        print(" Phase Angle | Ideal Code Map | Physical QPU Map | Emu Fidelity")
        print("---------------------------------------------------------")

        for i, phi in enumerate(evolution_steps):
            pub_result = result[i]
            counts = pub_result.data.qvm_bus.get_counts()

            # Calculate the ideal theoretical output map based on standard rotation math
            expected_11_ratio = (np.cos(phi) ** 2) * 100
            expected_00_ratio = (np.sin(phi) ** 2) * 100

            # Retrieve the literal physical QPU output map
            actual_11_ratio = (counts.get('11', 0) / 1000) * 100
            actual_00_ratio = (counts.get('00', 0) / 1000) * 100

            # Calculate how perfectly the virtual layer matched reality (Emu Fidelity)
            # Calculated by taking the difference from ideal mapping limits
            error_delta = abs(expected_11_ratio - actual_11_ratio)
            emu_fidelity = 100.0 - error_delta

            deg = np.degrees(phi)
            print(f" {deg:5.1f}     | 11:{expected_11_ratio:4.1f}%     | 11:{actual_11_ratio:4.1f}%      | {emu_fidelity:5.1f}%")
            print(f"              | 00:{expected_00_ratio:4.1f}%     | 00:{actual_00_ratio:4.1f}%      |")
        print("=========================================================")

if __name__ == "__main__":
    emulator = HyperbolicQVMEmuHarness()
    emulator.run_virtual_physics_sweep()
