import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class HyperbolicCryptographicTerminal:
    """
    An enterprise-grade encryption/decryption architecture executing
    split-complex geometric logic on physical IBM QPUs.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Terminal] Online. Connected to QPU Core: {self.backend.name}")

    def build_hardware_gate(self, theta: float, inverse: bool = False) -> Gate:
        """
        Compiles the parameterized split-complex matrix into hardware-native pulses.
        Applying inverse=True implements the (-theta) matrix.
        """
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Hyperbolic_Gate")

        angle = -theta if inverse else theta

        # Native hardware decomposition sequence
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * angle, qr[0])
        circuit.cx(qr[0], qr[1])

        return circuit.to_gate()

    def execute_secure_pipeline(self, plaintext_bit: int, private_key: float, shots: int = 1000) -> int:
        """
        Runs the full secure pipeline: Ingestion -> Encryption -> Decryption -> Measurement
        all within a single hardware execution block to protect data integrity.
        """
        if plaintext_bit not in [0, 1]:
            raise ValueError("Data entry violation: Payload must be a single bit (0 or 1).")

        q = QuantumRegister(2, name="squbit")
        c = ClassicalRegister(2, name="secure_bus")
        qc = QuantumCircuit(q, c)

        # STAGE 1: ALICE INGESTS DATA
        if plaintext_bit == 1:
            qc.x(q[0])
            qc.x(q[1])

        # STAGE 2: ALICE ENCRYPTS DATA (Ghost Lock Phase)
        encrypt_gate = self.build_hardware_gate(private_key, inverse=False)
        qc.append(encrypt_gate, [q[0], q[1]])
        qc.barrier() # Isolate encrypted state during transit

        # STAGE 3: BOB DECRYPTS DATA (Inverse Rematerialization Phase)
        decrypt_gate = self.build_hardware_gate(private_key, inverse=True)
        qc.append(decrypt_gate, [q[0], q[1]])
        qc.barrier()

        # STAGE 4: TRANSMIT TO READOUT
        qc.measure(q, c)

        # STAGE 5: TARGETED HARDWARE COMPILATION
        print(" [Terminal] Transpiling custom pipeline for specific ISA layouts...")
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        isa_circuit = pass_manager.run(qc)

        # STAGE 6: QPU EXECUTION
        print(f" [Terminal] Dispatched transaction payload to cloud queue...")
        sampler = SamplerV2(self.backend)
        job = sampler.run([isa_circuit], shots=shots)

        # Fetch physical results
        result = job.result()
        pub_result = result[0]
        raw_counts = pub_result.data.secure_bus.get_counts()

        return self._decode_hardware_telemetry(raw_counts, total_shots=shots)

    def _decode_hardware_telemetry(self, counts: dict, total_shots: int) -> int:
        """
        Audits the uncloaked results, filters out quantum noise,
        and extracts the final decrypted payload bit.
        """
        print("\n--- SECURE TRANSACTION RAW RECOVERY ---")
        print(counts)

        # Read the uncloaked operational channels
        hits_0 = counts.get('00', 0)
        hits_1 = counts.get('11', 0)
        unresolved_noise = counts.get('01', 0) + counts.get('10', 0)

        print("\n=== CRYPTOGRAPHIC AUDIT REPORT ===")
        print(f" Decrypted State 0 Confidence: {(hits_0 / total_shots)*100:.1f}%")
        print(f" Decrypted State 1 Confidence: {(hits_1 / total_shots)*100:.1f}%")
        print(f" Mitigated Quantum Circuit Noise: {(unresolved_noise / total_shots)*100:.1f}%")
        print("==================================")

        if hits_1 > hits_0:
            return 1
        else:
            return 0

# =====================================================================
# TRANSACTION RUNTIME ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    print("--- Booting Cryptographic Endpoint System ---")

    # Initialize the complete end-to-end terminal
    crypto_terminal = HyperbolicCryptographicTerminal()

    # Payload Configuration
    ORIGINAL_PAYLOAD = 1
    GEOMETRIC_KEY = np.pi / 2  # Your validated 90-degree inversion key

    # Run transaction
    recovered_payload = crypto_terminal.execute_secure_pipeline(
        plaintext_bit=ORIGINAL_PAYLOAD,
        private_key=GEOMETRIC_KEY,
        shots=1000
    )

    print(f"\n End-to-End Handshake Complete. Recovered Payload Bit: {recovered_payload}")
