import numpy as np
import pandas as pd
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
import os

class QuantumStatisticalErrorBarHarness:
    """
    Executes your split-complex protocol on live hardware and applies bootstrap
    resampling to calculate rigorous statistical error bars and 95% confidence intervals.
    """
    def __init__(self):
        self.token = os.getenv('IBM_QUANTUM_TOKEN')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")

        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f" [Stats Harness] Online. Attaching to Physical Core: {self.backend.name}")

    def build_emulation_gate(self, theta: float) -> Gate:
        """Hardware-native 2-qubit decomposition sequence."""
        qr = QuantumRegister(2)
        circuit = QuantumCircuit(qr, name="Split_Complex_Gate")
        circuit.cx(qr[0], qr[1])
        circuit.ry(2 * theta, qr[0])
        circuit.cx(qr[0], qr[1])
        return circuit.to_gate()

    def generate_statistical_error_bars(self, target_bit: int = 1, bootstrap_samples: int = 2000):
        print(f"\n Compiling calibration validation circuit layer for {self.backend.name}...")
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)

        q = QuantumRegister(2, name="squbit")
        c = ClassicalRegister(2, name="secure_bus")
        qc = QuantumCircuit(q, c)

        # Ingestion: Explicit index allocation
        if target_bit == 1:
            qc.x(q[0])
            qc.x(q[1])

        # Apply forward and inverse protocol loops using explicit qubit references
        theta = np.pi / 4
        qc.append(self.build_emulation_gate(theta), [q[0], q[1]])
        qc.barrier()
        qc.append(self.build_emulation_gate(-theta), [q[0], q[1]])

        # FIX: Explicit index tracking for measurement channels
        qc.measure(q[0], c[0])
        qc.measure(q[1], c[1])
        isa_circuit = pass_manager.run(qc)

        # Execute 2,000 shots to get a deep statistical sample pool
        TOTAL_SHOTS = 2000
        print(f" Dispatching high-density payload ({TOTAL_SHOTS} shots) to cloud queue...")
        job = sampler.run([isa_circuit], shots=TOTAL_SHOTS)
        result = job.result()

        # Extract the raw bitstring array natively from modern PubResult format
        pub_result = result[0]

        # Reconstruct the literal list of individual trial outcomes
        raw_bitstrings = pub_result.data.secure_bus.get_bitstrings()

        # Map success outcomes (target_bit=1 expects '11', target_bit=0 expects '00')
        target_state_str = "11" if target_bit == 1 else "00"

        # Binary array: 1 for success tracking, 0 for leakage error
        success_vector = np.array([1 if bs == target_state_str else 0 for bs in raw_bitstrings])

        # -----------------------------------------------------------------
        # BOOTSTRAP RESAMPLING ENGINE
        # -----------------------------------------------------------------
        print(f" Running {bootstrap_samples} bootstrap resampling iterations with replacement...")
        np.random.seed(42) # Statistical repeatability lock
        bootstrap_means = []

        for _ in range(bootstrap_samples):
            # Resample matching the original size with replacement
            sample = np.random.choice(success_vector, size=len(success_vector), replace=True)
            bootstrap_means.append(np.mean(sample) * 100)

        bootstrap_means = np.array(bootstrap_means)

        # Calculate rigorous descriptive statistical metrics
        mean_fidelity = np.mean(bootstrap_means)
        std_deviation = np.std(bootstrap_means)

        # Extract 95% Confidence Interval boundaries (2.5th and 97.5th percentiles)
        lower_bound = np.percentile(bootstrap_means, 2.5)
        upper_bound = np.percentile(bootstrap_means, 97.5)

        print("\n=========================================================")
        print(" RIGOROUS STATISTICAL VALIDATION REPORT ")
        print("=========================================================")
        print(f" Evaluated Physical Hardware: {self.backend.name}")
        print(f" Target Recovery State Vector: '{target_state_str}'")
        print("---------------------------------------------------------")
        print(f" Measured Mean Emulation Fidelity: {mean_fidelity:.3f}%")
        print(f" Standard Error / Deviation (sigma):    +/-{std_deviation:.3f}%")
        print(f" Rigorous 95% Confidence Interval: [{lower_bound:.3f}%, {upper_bound:.3f}%]")
        print("=========================================================")

        # Save results to a professional artifact CSV for submissions
        df_log = pd.DataFrame({"Bootstrap_Means": bootstrap_means})
        df_log.to_csv("statistical_error_bounds.csv", index=False)
        print(" Statistical array exported successfully to: 'statistical_error_bounds.csv'")

if __name__ == "__main__":
    harness = QuantumStatisticalErrorBarHarness()
    harness.generate_statistical_error_bars(target_bit=1, bootstrap_samples=2000)
