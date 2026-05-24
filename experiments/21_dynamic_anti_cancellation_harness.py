import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class DynamicAntiCancellationHarness:
    """
    Implements a mid-circuit measurement-conditioned execution loop.
    Forces physical QPU gate execution by blinding the compiler's analytical solvers.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Anti-Cancel Rig] Online. Attached to Live QPU: {self.backend.name}")

    def build_emulation_gate(self, theta: float, inverse: bool = False) -> Gate:
        """Hardware-native 2-qubit decomposition sequence."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Split_Complex_Gate")
        angle = -theta if inverse else theta
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * angle, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def execute_dynamic_verification(self):
        print("\n Assembling Dynamic Mid-Circuit Conditional Branching Array...")
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        # Allocate 3 Qubits:
        # q[0], q[1] = Your Core Emulation Squbit Register
        # q[2]       = The Dynamic Mid-Circuit Hardware Trigger
        q = QuantumRegister(3, name="hardware_qubits")
        c_trigger = ClassicalRegister(1, name="mid_circuit_trigger")
        c_bus = ClassicalRegister(2, name="secure_bus")
        qc = QuantumCircuit(q, c_trigger, c_bus)

        # 1. DATA INGESTION (Initialize core registers to State 11)
        qc.x(q[0])
        qc.x(q[1])
        qc.barrier()

        # 2. SEPARATED ENCRYPTION TRACK
        f_gate = self.build_emulation_gate(np.pi/4, inverse=False)
        qc.append(f_gate, [q[0], q[1]])
        qc.barrier()

        # 3. MID-CIRCUIT HARDWARE TRIGGER GENERATION
        # Put qubit 2 into an unpredictable 50/50 hardware state
        qc.h(q[2])
        # Physically measure qubit 2 MID-RUN. This halts compiler optimization dead.
        qc.measure(q[2], c_trigger[0])
        qc.barrier()

        # 4. THE DYNAMIC COMPILER TRAP (Conditional Dynamic Execution)
        # The hardware reads c_trigger at runtime. Optimization cannot bypass this block.
        r_gate = self.build_emulation_gate(np.pi/4, inverse=True)

        with qc.if_test((c_trigger, 1)):
            print(" Injecting runtime conditional True path (Executing Inverse Gate Matrix)...")
            qc.append(r_gate, [q[0], q[1]])
        with qc.if_test((c_trigger, 0)):
            print(" Injecting runtime conditional False path (Executing Alternative Phase Rotation)...")
            # Alternate vector line to guarantee the compiler must preserve both code paths
            qc.rz(np.pi/4, q[0])
            qc.append(r_gate, [q[0], q[1]])

        qc.barrier()

        # Final payload readout mapping
        qc.measure(q[0], c_bus[0])
        qc.measure(q[1], c_bus[1])

        print(f"  Compiling dynamic hardware loops for {self.backend.name} ISA architecture...")
        isa_circuit = pass_manager.run(qc)

        # --- RIGOROUS RESOURCE PROOF ---
        print("\n=========================================================")
        print(" POST-TRANSPILE HARDWARE INSTRUCTION PROOF ")
        print("=========================================================")
        print(f" Native Operations Array: {isa_circuit.count_ops()}")
        print(f" Compiled Hardware Depth: {isa_circuit.depth()}")
        print(f" Structural Circuit Size: {isa_circuit.size()}")
        print("=========================================================\n")

        print(f" Transmitting payload network to {self.backend.name} queue...")
        job = sampler.run([isa_circuit], shots=1000)
        result = job.result()

        # Parse data out of the specific PubResult block
        pub_result = result[0]
        counts_bus = pub_result.data.secure_bus.get_counts()
        counts_trigger = pub_result.data.mid_circuit_trigger.get_counts()

        # Quantify target recovery rate
        fidelity = (counts_bus.get('11', 0) / 1000) * 100

        print("=========================================================")
        # if_test execution requires modern hardware to pass successfully
        print(" UN-OPTIMIZABLE PHYSICAL TELEMETRY REPORT")
        print("=========================================================")
        print(f" Mid-Circuit Random Trigger Layout Counts: {counts_trigger}")
        print(f" Verified Subspace Emulation Fidelity:      {fidelity:.1f}%")
        print(f" Raw Hardware Register Fingerprint:         {counts_bus}")
        print("=========================================================")

if __name__ == "__main__":
    harness = DynamicAntiCancellationHarness()
    harness.execute_dynamic_verification()
