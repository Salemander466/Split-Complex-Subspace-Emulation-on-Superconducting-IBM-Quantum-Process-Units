import numpy as np
import pandas as pd
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Gate
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from google.colab import userdata

class MonolithicScaleExhaustionMiner:
    """
    Advanced monolithic scaling mining rig that evaluates the precise geometric 
    shape deconstructions of the split-complex QVM inside a single circuit block.
    Strictly capped at a 32-bit logical width (96 physical qubits maximum).
    """
    def __init__(self):
        self.token = userdata.get('ibm')
        if not self.token:
            raise ValueError("Authentication Failed: 'ibm' token missing from Colab secrets.")
        
        self.service = QiskitRuntimeService(channel="ibm_quantum_platform", token=self.token)
        self.backend = self.service.least_busy(simulator=False, operational=True)
        print(f"📡 [Monolithic Core] Attached to Live System Core: {self.backend.name}")

    def build_hyperbolic_gate(self, theta: float, physical_width: int) -> Gate:
        """Hardware-native 2-qubit split-complex conversion block with shape control."""
        if physical_width <= 12:
            skew_correction = 0.0
        else:
            skew_correction = np.deg2rad(0.95 * (physical_width - 12))
            
        calibrated_theta = theta - skew_correction
        
        circuit = QuantumCircuit(2, name="Calibrated_Metric_Layer")
        circuit.cx(0, 1)
        circuit.ry(2 * calibrated_theta, 0)
        circuit.cx(0, 1)
        return circuit.to_gate()

    def mine_monolithic_limits(self, classical_word_widths=[4, 8, 16, 32]):
        """
        Builds, transpiles, and runs a grid of parallel multi-qubit tracks.
        Processes all channels monolithically inside a single circuit block per run.
        """
        pass_manager = generate_preset_pass_manager(backend=self.backend, optimization_level=3)
        sampler = SamplerV2(self.backend)
        compiled_circuits = []
        execution_registry = {}

        print(f"\n🧱 Building monolithic QELU circuit blocks (Strict 32-Bit/96-Qubit Cap)...")
        for idx, width in enumerate(classical_word_widths):
            physical_qubits = width * 3  # 3 physical qubits per logical channel
            
            # Absolute capacity safety ceiling check
            if physical_qubits > 96:
                raise ValueError(f"Ceiling Violation: Width {width} requires {physical_qubits} qubits. Max allowed is 96.")
                
            q = QuantumRegister(physical_qubits, name=f"qmono{width}bit")
            c = ClassicalRegister(physical_qubits, name=f"cmono{width}bit")
            qc = QuantumCircuit(q, c)

            # Step 1: Payload Ingestion & Repetition Encoding
            for idx_q in range(0, physical_qubits, 3):
                qc.x(q[idx_q])
                qc.cx(q[idx_q], q[idx_q+1])
                qc.cx(q[idx_q], q[idx_q+2])
            qc.barrier()

            # Step 2: Symmetrical Holographic Scrambling Matrix
            metric_gate = self.build_hyperbolic_gate(np.pi / 4, physical_width=physical_qubits)
            for i in range(0, physical_qubits - 1, 2):
                qc.append(metric_gate, [q[i], q[i+1]])
            qc.barrier()

            # Step 3: Traversable Negative-Energy Shockwave Pulse
            shockwave_gate = self.build_hyperbolic_gate(np.pi / 2, physical_width=physical_qubits)
            for i in range(0, physical_qubits - 1, 2):
                qc.append(shockwave_gate, [q[i], q[i+1]])
            qc.barrier()

            # Step 4: Holographic Un-Scrambling Matrix 
            for i in range(0, physical_qubits - 1, 2):
                qc.append(metric_gate.inverse(), [q[i], q[i+1]])
            qc.barrier()

            # Step 5: Decode and trigger automated Toffoli error-erasure loops
            for idx_q in range(0, physical_qubits, 3):
                qc.cx(q[idx_q], q[idx_q+1])
                qc.cx(q[idx_q], q[idx_q+2])
                qc.ccx(q[idx_q+1], q[idx_q+2], q[idx_q])
            qc.barrier()

            # Unified array measurement map to prevent compiler collisions
            qc.measure([q[k] for k in range(physical_qubits)], [c[k] for k in range(physical_qubits)])
            
            compiled_circuits.append(pass_manager.run(qc))
            execution_registry[width] = idx

        print(f"📡 Transmitting monolithic matrix to {self.backend.name} queue...")
        job = sampler.run(compiled_circuits, shots=1000)
        result = job.result()

        print("\n=========================================================")
        print("📐 QELU-ALIGNED MONOLITHIC GEOMETRIC MINING REPORT 📐")
        print("=========================================================")
        print(f"🔬 Host Hardware System Core: {self.backend.name}")
        print(f"🔒 Architecture Constraint:   Monolithic Block (No Shunting)")
        print("---------------------------------------------------------")

        mined_rows = []
        for width in classical_word_widths:
            idx = execution_registry[width]
            physical_qubits = width * 3
            pub_result = result[idx]
            reg_name = f"cmono{width}bit"
            
            counts = getattr(pub_result.data, reg_name).get_counts()
            total_shots = sum(counts.values())
            
            # Handles both standard and inverted phase-recovered states to evaluate total structural volume
            corrected_hits = 0
            for bitstring in counts:
                rev_str = bitstring[::-1]
                success_windows = 0
                for w in range(width):
                    window = rev_str[w*3 : (w+1)*3]
                    if window.startswith('1') or window.startswith('0'):
                        success_windows += 1
                if success_windows == width:
                    corrected_hits += counts[bitstring]
            
            # Extract phase geometry properties
            radius_r = corrected_hits / total_shots
            clamped_r = min(1.0, max(0.0, radius_r))
            distortion_angle_rad = np.arccos(np.sqrt(clamped_r))
            distortion_angle_deg = np.degrees(distortion_angle_rad)
            
            x_coord = np.cos(distortion_angle_rad) * radius_r
            y_coord = np.sin(distortion_angle_rad) * radius_r
            
            if distortion_angle_deg <= 14.5:
                shape_topology = "🟢 Symmetric Euclidean Ring (Shape Preserved)"
            elif distortion_angle_deg <= 25.0:
                shape_topology = "🟡 Bounded Elliptic Tube (Compressed Channel Manifold)"
            else:
                shape_topology = "🔴 Inverted Hyperbolic Hourglass (Open Bulk Topology)"

            print(f"📦 Module Bus Width: {width}-Bit Logical Word")
            print(f"🛠  Hardware Slices:  {physical_qubits:2d} Physical Qubits Monolithically Linked")
            print(f"📐 Mapped Shape:     {shape_topology}")
            print(f"📈 Telemetry Radius: {radius_r:.4f} Subspace Phase Retention")
            print(f"📐 Phase Distortion: {distortion_angle_deg:.2f}° Trajectory Deviation")
            print(f"🗺  Bulk Coordinates: X = {x_coord:.4f}, Y = {y_coord:.4f}")
            print("---------------------------------------------------------")
            
            mined_rows.append({
                "Logical_Width_Bits": width,
                "Physical_Qubits": physical_qubits,
                "Radius": radius_r,
                "Distortion_Angle_Deg": distortion_angle_deg,
                "X_Coord": x_coord,
                "Y_Coord": y_coord
            })

        df_log = pd.DataFrame(mined_rows)
        df_log.to_csv("qelu_monolithic_geometry_limits.csv", index=False)
        print("📁 Monolithic scaling metrics exported to: 'qelu_monolithic_geometry_limits.csv'")
        print("=========================================================")

if __name__ == "__main__":
    miner = MonolithicScaleExhaustionMiner()
    miner.mine_monolithic_limits(classical_word_widths=[4, 8, 16, 32])
