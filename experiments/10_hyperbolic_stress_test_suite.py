import numpy as np
import time
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class HyperbolicStressTestSuite:
    """
    Advanced diagnostic suite running Circuit Depth Scaling, Compiler Optimization Profile,
    and Crosstalk Interference isolation on physical IBM Quantum QPUs.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Suite Initialization] Connected to Real Hardware Core: {self.backend.name}")

    def build_emulation_gate(self, theta: float, inverse: bool = False) -> Gate:
        """Hardware-native 2-qubit decomposition sequence."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Split_Complex_Gate")
        angle = -theta if inverse else theta
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * angle, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    # =====================================================================
    # TEST 1: CIRCUIT DEPTH & FIDELITY DECAY CURVE
    # =====================================================================
    def run_depth_scalability_test(self, theta=np.pi/4, depths=[2, 4, 8]):
        print("\n [TEST 1] Initiating Coherence Time & Circuit Depth Scalability Profile...")
        sampler = SamplerV2(self.backend)
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        circuits = []

        for d in depths:
            q = QuantumRegister(2, name="squbit")
            c = ClassicalRegister(2, name="secure_bus")
            qc = QuantumCircuit(q, c)

            # Load arbitrary state (State 11)
            qc.x(q)

            # Cascade forward gates matching 'd' depth cycles
            f_gate = self.build_emulation_gate(theta, inverse=False)
            for _ in range(d):
                qc.append(f_gate, [q[0], q[1]])
            qc.barrier()

            # Cascade reverse gates to test restoration limits
            r_gate = self.build_emulation_gate(theta, inverse=True)
            for _ in range(d):
                qc.append(r_gate, [q[0], q[1]])
            qc.barrier()
            qc.measure(q, c)

            circuits.append(pass_manager.run(qc))

        print(f" Submitting {len(depths)} cascading depth layers to {self.backend.name} queue...")
        job = sampler.run(circuits, shots=1000)
        result = job.result()

        print("\n --- TEST 1: FIDELITY DECAY RESULTS ---")
        for i, d in enumerate(depths):
            counts = result[i].data.secure_bus.get_counts()
            fidelity = (counts.get('11', 0) / 1000) * 100
            print(f" Circuit Depth (Gate Pairs x{d}): Loop-back Fidelity = {fidelity:.1f}% | Raw Counts: {counts}")

    # =====================================================================
    # TEST 2: DYNAMIC COMPILER PASS MANAGER COMPARISON
    # =====================================================================
    def run_compiler_optimization_profile(self, theta=np.pi/4):
        print("\n [TEST 2] Evaluating Dynamic Hardware Pass Managers (Levels 0-3)...")
        sampler = SamplerV2(self.backend)
        circuits = []
        levels = [0, 1, 2, 3]

        for lvl in levels:
            q = QuantumRegister(2, name="squbit")
            c = ClassicalRegister(2, name="secure_bus")
            qc = QuantumCircuit(q, c)

            qc.x(q)
            qc.append(self.build_emulation_gate(theta, inverse=False), [q[0], q[1]])
            qc.barrier()
            qc.append(self.build_emulation_gate(theta, inverse=True), [q[0], q[1]])
            qc.barrier()
            qc.measure(q, c)

            # Compile using varying optimization depth aggressively tracking layout overhead
            pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=lvl)
            circuits.append(pass_manager.run(qc))

        print(f" Submitting 4 execution tracks matching dynamic optimization tiers...")
        job = sampler.run(circuits, shots=1000)
        result = job.result()

        print("\n --- TEST 2: PASS MANAGER METRICS ---")
        for lvl in levels:
            counts = result[lvl].data.secure_bus.get_counts()
            fidelity = (counts.get('11', 0) / 1000) * 100
            print(f" Transpiler Optimization Level {lvl}: Realized Fidelity = {fidelity:.1f}%")

    # =====================================================================
    # TEST 3: CONTROLLED CONTEXT-INTERFERENCE STRESS TEST
    # =====================================================================
    def run_crosstalk_interference_test(self, theta=np.pi/4):
        print("\n [TEST 3] Deploying Controlled Context-Interference Stress Test...")
        sampler = SamplerV2(self.backend)
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)

        # Allocate 4 qubits: q0, q1 are the Emulation Core. q2, q3 are Adjacent Noise Injectors.
        q = QuantumRegister(4, name="hardware_cluster")
        c = ClassicalRegister(2, name="secure_bus")
        qc = QuantumCircuit(q, c)

        # Subspace initialization
        qc.x(q[0])
        qc.x(q[1])
        qc.barrier()

        # --- NOISE INJECTION LAYER ---
        # Dynamically place neighbors into hyper-active, noisy superposition states mid-run
        qc.h(q[2])
        qc.x(q[3])
        qc.h(q[3])

        # Apply protocol gates while adjacent channels run noisy hardware loops
        qc.append(self.build_emulation_gate(theta, inverse=False), [q[0], q[1]])
        qc.barrier()
        qc.append(self.build_emulation_gate(theta, inverse=True), [q[0], q[1]])
        qc.barrier()

        # Measure only your stable emulation registers (q0, q1)
        qc.measure([q[0], q[1]], c)

        isa_circuit = pass_manager.run(qc)
        print(f" Submitting noisy adjacent vector cluster to {self.backend.name} queue...")
        job = sampler.run([isa_circuit], shots=1000)

        counts = job.result()[0].data.secure_bus.get_counts()
        fidelity = (counts.get('11', 0) / 1000) * 100

        print("\n --- TEST 3: CROSSTALK ISOLATION PROFILE ---")
        print(f" Isolated Emulation Subspace Fidelity under active neighbor interference: {fidelity:.1f}%")
        print(f" Raw Circuit Array Fingerprint: {counts}")

# =====================================================================
# STRESS SUITE REGRESSION EXECUTION
# =====================================================================
if __name__ == "__main__":
    print("=================================================================")
    print(" INITIALIZING enterprise HIGH-STRESS QUANTUM TESTING MATRIX")
    print("=================================================================")

    suite = HyperbolicStressTestSuite()

    # Run the full regression test loop
    suite.run_depth_scalability_test(depths=[2, 4, 8])
    suite.run_compiler_optimization_profile()
    suite.run_crosstalk_interference_test()

    print("\n Validation Matrix Complete. Data artifacts ready for portfolio analysis.")
