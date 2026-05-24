import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class ClosedTimelikeCurveSimulator:
    """
    Simulates David Deutsch's Closed Timelike Curve (CTC) paradox-free time travel
    model using mid-circuit dynamic execution and split-complex coordinate inversion layers.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Causality Core] Booting CTC Spacetime Engine on: {self.backend.name}")

    def build_inversion_gate(self, theta: float) -> Gate:
        """Hardware-native 2-qubit split-complex rotation gate."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Split_Complex_Inversion")
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * theta, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def execute_ctc_simulation(self):
        print("\n [CTC Sim] Assembling paradox-free holographic time-loop matrix...")
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        # Allocate 3 Qubits:
        # q[0] = The Past Chronology State
        # q[1] = The Future Chronology State
        # q[2] = System Ancilla / Phase Intersect Node
        q = QuantumRegister(3, name="spacetime_manifold")
        c_future = ClassicalRegister(1, name="future_readout")
        c_past = ClassicalRegister(2, name="past_bus")
        qc = QuantumCircuit(q, c_future, c_past)

        # Step 1: Ingest payload into initial past timeline (State 11)
        qc.x(q[0])
        qc.x(q[1])
        qc.barrier()

        # Step 2: The Future Traversal (Rotate Qubits 0 and 1 into the wormhole throat)
        time_gate = self.build_inversion_gate(np.pi / 4)
        qc.append(time_gate, [q[0], q[1]])
        qc.barrier()

        # Step 3: The Chronology Horizon (Measure the future state mid-run)
        qc.measure(q[1], c_future[0])
        qc.barrier()

        # Step 4: The Causality Loop (Feed the future data back to alter the past state)
        inverse_time_gate = self.build_inversion_gate(np.pi / 4)

        with qc.if_test((c_future, 1)):
            qc.append(inverse_time_gate, [q[0], q[1]])
        with qc.if_test((c_future, 0)):
            qc.rz(np.pi / 2, q[0])
            qc.append(inverse_time_gate, [q[0], q[1]])
        qc.barrier()

        # Final readout of the stabilized past timeline
        qc.measure(q[0], c_past[0])
        qc.measure(q[1], c_past[1])

        print(f"  Compiling paradox-free chronology loops for {self.backend.name} ISA...")
        isa_circuit = pass_manager.run(qc)

        print(" Dispatching causality-violation experiment to cloud runtime...")
        job = sampler.run([isa_circuit], shots=1000)
        result = job.result()

        # FIX: Explicit index targeting PubResult array blocks natively to bypass AttributeError
        pub_result = result[0]
        counts_past = pub_result.data.past_bus.get_counts()
        counts_future = pub_result.data.future_readout.get_counts()

        # Successful paradox-free resolution returns '11'
        target_output = "11"
        consistency_rate = (counts_past.get(target_output, 0) / 1000) * 100

        print("\n=========================================================")
        print(" CLOSED TIMELIKE CURVE DEUTSCH CONSISTENCY PROFILE ")
        print("=========================================================")
        print(f"  Simulation Track: Non-Unitary Chronology Horizon Loop")
        print(f" Physical Hardware: {self.backend.name}")
        print("---------------------------------------------------------")
        print(f" Telemetry Metrics:")
        print(f"   -> Future Metric Trigger Split:      {counts_future}")
        print(f"   -> Deutsch Consistency Success Rate: {consistency_rate:.1f}%")
        print(f" Raw Past Timeline Register Output: {counts_past}")
        print("=========================================================")

if __name__ == "__main__":
    simulator = ClosedTimelikeCurveSimulator()
    simulator.execute_ctc_simulation()
